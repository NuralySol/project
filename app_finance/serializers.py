from .models import Profile, Transaction
from rest_framework import serializers

# Serializer for Profile model
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'plaid_access_token']

# Serializer for Transaction model. 
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'user',
            'plaid_transaction_id',
            'category',
            'amount',
            'description',
            'date',
        ]  