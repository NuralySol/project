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
import logging

# Create a logger object
logger = logging.getLogger(__name__)

# Home page: Display the list of transactions (if any)
def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'finance/transaction_list.html', {'transactions': transactions})

@login_required
def fetch_transactions(request):
    try:
        access_token = request.user.profile.plaid_access_token
        if not access_token:
            raise ValueError("Access token not found for the user.")

        start_date = date(2024, 7, 27)  # Ensure this is a valid date object
        end_date = date.today()

        # Debugging: Print request parameters
        print(f"DEBUG: Access Token: {access_token}")
        print(f"DEBUG: Start Date: {start_date}")
        print(f"DEBUG: End Date: {end_date}")

        request_body = TransactionsGetRequest(
            access_token=access_token,
            start_date=start_date,
            end_date=end_date
        )

        # Debugging: Print the request body
        print(f"DEBUG: TransactionsGetRequest: {request_body}")

        response = client.transactions_get(request_body)
        response_dict = response.to_dict()

        # Debugging: Print the full response from Plaid
        print(f"DEBUG: Full TransactionsGet Response: {response_dict}")

        transactions = response_dict.get("transactions", [])
        
        # Debugging: Print the extracted transactions
        print(f"DEBUG: Extracted Transactions: {transactions}")

        if not transactions:
            print("DEBUG: No transactions found in the API response.")

        return render(request, 'finance/plaid_transactions.html', {'transactions': transactions})
    except Exception as e:
        # Debugging: Print the error message
        print(f"ERROR: Error fetching transactions: {e}")
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

# Dashboard: Display user's transactions or option to create a sandbox account
@login_required
def dashboard(request):
    from plaid.model.transactions_get_request import TransactionsGetRequest
    import logging

    logger = logging.getLogger(__name__)
    transactions = []
    try:
        access_token = request.user.profile.plaid_access_token
        start_date = date(2024, 1, 1)
        end_date = date.today()

        request_body = TransactionsGetRequest(
            access_token=access_token,
            start_date=start_date,
            end_date=end_date
        )
        response = client.transactions_get(request_body)
        transactions = response.to_dict().get("transactions", [])

        logger.info(f"Transactions fetched: {transactions}")
    except Exception as e:
        logger.error(f"Error fetching transactions: {str(e)}")
        messages.error(request, f"Error fetching transactions: {str(e)}")

    return render(request, 'finance/dashboard.html', {'transactions': transactions})
# Create a sandbox item and return JSON response
@login_required
def create_sandbox_item(request):
    try:
        request_body = SandboxPublicTokenCreateRequest(
            institution_id='ins_109508',
            initial_products=[Products('transactions')],
            options={
                "override_username": "custom_nuraly"
            }
        )
        response = client.sandbox_public_token_create(request_body)
        logger.info(f"Sandbox Public Token Response: {response}")

        public_token = response.public_token

        # Exchange the public token for an access token
        exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
        exchange_response = client.item_public_token_exchange(exchange_request)
        access_token = exchange_response.access_token

        # Save the access token
        request.user.profile.plaid_access_token = access_token
        request.user.profile.save()

        messages.success(request, "Custom sandbox user connected successfully!")
        return JsonResponse({"success": True, "access_token": access_token})
    except Exception as e:
        logger.error(f"Error creating sandbox item: {str(e)}")
        return JsonResponse({"success": False, "error": str(e)})

# Plaid sandbox setup and redirection
@login_required
def plaid_sandbox(request):
    client = plaid_api.PlaidApi()
    try:
        pt_request = SandboxPublicTokenCreateRequest(
            institution_id='ins_109508',
            initial_products=[Products('transactions')]
        )
        pt_response = client.sandbox_public_token_create(pt_request)
        public_token = pt_response.to_dict()['public_token']

        exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
        exchange_response = client.item_public_token_exchange(exchange_request)

        access_token = exchange_response.to_dict()['access_token']

        # Store access token in user's profile
        request.user.profile.plaid_access_token = access_token
        request.user.profile.save()

        messages.success(request, "Sandbox account linked successfully!")
        return redirect('dashboard')

    except Exception as e:
        messages.error(request, f"Error linking sandbox account: {str(e)}")
        return redirect('dashboard')
    
