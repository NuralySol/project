from plaid.configuration import Configuration
from plaid.api_client import ApiClient
from plaid.api import plaid_api
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

configuration = Configuration(
    host=settings.PLAID_ENV,
    api_key={
        'clientId': settings.PLAID_CLIENT_ID,
        'secret': settings.PLAID_SECRET,
    }
)
api_client = ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

logger.info(f"PLAID_CLIENT_ID: {settings.PLAID_CLIENT_ID}")
logger.info(f"PLAID_SECRET: {settings.PLAID_SECRET}")