from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from .models import Transaction
from plaid.api import plaid_api
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.products import Products
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from app_finance.plaid_client import client
from datetime import date
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializers import TransactionSerializer, ProfileSerializer
import logging
import json
import time
from plaid.exceptions import ApiException

# Logger setup
logger = logging.getLogger(__name__)

class TransactionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user.profile)
        return Response(serializer.data)

# Home page
def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'finance/transaction_list.html', {'transactions': transactions})

@login_required
def fetch_transactions(request):
    try:
        access_token = request.user.profile.plaid_access_token
        if not access_token:
            messages.error(request, "Access token not found. Please link a sandbox account first.")
            return redirect('plaid_sandbox')

        start_date = date(2024, 1, 1)
        end_date = date.today()

        for _ in range(3):  # Retry up to 3 times
            try:
                # Request transactions from Plaid
                request_body = TransactionsGetRequest(
                    access_token=access_token,
                    start_date=start_date,
                    end_date=end_date
                )

                response = client.transactions_get(request_body)
                response_dict = response.to_dict()

                # Extract transactions and serialize date fields
                transactions = response_dict.get("transactions", [])
                serialized_transactions = [
                    {
                        **t,
                        "date": t.get("date").isoformat() if t.get("date") else None,
                        "authorized_date": t.get("authorized_date").isoformat() if t.get("authorized_date") else None
                    }
                    for t in transactions
                ]

                # Pass the serialized transactions to the template
                return render(request, 'finance/plaid_transactions.html', {'transactions': serialized_transactions})

            except ApiException as e:
                error_response = json.loads(e.body)
                error_code = error_response.get("error_code", "UNKNOWN")
                if error_code == "PRODUCT_NOT_READY":
                    logger.warning("Product not ready, retrying in 5 seconds...")
                    time.sleep(5)  # Wait 5 seconds before retrying
                else:
                    raise

        messages.error(request, "Transactions are not ready. Please try again later.")
        return redirect('dashboard')

    except ApiException as e:
        error_response = json.loads(e.body)
        error_message = error_response.get("error_message", "Unknown error")
        logger.error(f"Plaid API error: {error_message}", exc_info=True)
        messages.error(request, f"Plaid API error: {error_message}")
    except Exception as e:
        logger.error(f"Error fetching transactions: {e}", exc_info=True)
        messages.error(request, f"Error fetching transactions: {str(e)}")

    return redirect('dashboard')

# Landing page
def landing_page(request):
    return render(request, 'finance/landing_page.html')

# User signup page
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'finance/signup.html', {'form': form})

@login_required
def dashboard(request):
    transactions = []
    try:
        access_token = request.user.profile.plaid_access_token
        if not access_token:
            raise ValueError("Access token not found for the user. Connect a sandbox item first.")

        # Dates for transactions
        start_date = date(2024, 1, 1)
        end_date = date.today()

        logger.info(f"Fetching transactions for {request.user.username} with access token: {access_token}")

        # Create the request to fetch transactions
        request_body = TransactionsGetRequest(
            access_token=access_token,
            start_date=start_date,
            end_date=end_date
        )
        logger.debug(f"TransactionsGetRequest Body: {request_body}")

        # Fetch transactions from Plaid
        response = client.transactions_get(request_body)
        response_dict = response.to_dict()

        # Log the full response for debugging
        logger.debug(f"Full Transactions API Response: {response_dict}")

        # Extract and serialize transactions
        transactions = response_dict.get("transactions", [])
        serialized_transactions = json.dumps([
            {
                **t,
                "date": str(t.get("date")) if t.get("date") else None,  # Ensure date is serialized as a string
                "authorized_date": str(t.get("authorized_date")) if t.get("authorized_date") else None  # Ensure authorized_date is serialized as a string
            }
            for t in transactions
        ])
        logger.debug(f"Serialized Transactions for Template: {serialized_transactions}")

        # Pass the serialized transactions to the template
        return render(request, 'finance/dashboard.html', {'transactions_json': serialized_transactions})

    except ApiException as e:
        error_response = json.loads(e.body)
        error_message = error_response.get("error_message", "Unknown error")
        logger.error(f"Plaid API error: {error_message}", exc_info=True)
        messages.error(request, f"Plaid API error: {error_message}")
    except Exception as e:
        logger.error(f"Error fetching transactions: {e}", exc_info=True)
        messages.error(request, f"Error fetching transactions: {str(e)}")

    return render(request, 'finance/dashboard.html', {'transactions_json': '[]'})

@login_required
def plaid_sandbox(request):
    try:
        pt_request = SandboxPublicTokenCreateRequest(
            institution_id='ins_109508',
            initial_products=[Products('transactions')]
        )
        pt_response = client.sandbox_public_token_create(pt_request)
        public_token = pt_response.public_token

        exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
        exchange_response = client.item_public_token_exchange(exchange_request)

        access_token = exchange_response.access_token
        request.user.profile.plaid_access_token = access_token
        request.user.profile.save()

        messages.success(request, "Sandbox account linked successfully!")
        return redirect('dashboard')
    except Exception as e:
        logger.error(f"Error linking sandbox account: {e}", exc_info=True)
        messages.error(request, f"Error linking sandbox account: {str(e)}")
        return redirect('dashboard')

@login_required
def create_sandbox_item(request):
    try:
        request_body = SandboxPublicTokenCreateRequest(
            institution_id='ins_109508',
            initial_products=[Products('transactions')]
        )

        response = client.sandbox_public_token_create(request_body)
        public_token = response.public_token

        exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
        exchange_response = client.item_public_token_exchange(exchange_request)
        access_token = exchange_response.access_token

        request.user.profile.plaid_access_token = access_token
        request.user.profile.save()

        return JsonResponse({"success": True, "access_token": access_token})
    except Exception as e:
        logger.error(f"Error creating sandbox item: {e}", exc_info=True)
        return JsonResponse({"success": False, "error": str(e)})

