from django.contrib import admin
from .models import Transaction, Profile

# Register your models here.
admin.site.register(Profile)
admin.site.register(Transaction)
