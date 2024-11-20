from django.shortcuts import render
from .models import Transaction
# Create your views here.

# This view will be used to display the list of transactions. It will be the home page of the application.
def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'finance/transaction_list.html', {'transactions': transactions})