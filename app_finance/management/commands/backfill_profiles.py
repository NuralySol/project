from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app_finance.models import Profile


class Command(BaseCommand):
    help = "Backfill profiles for existing users without a profile"

    def handle(self, *args, **kwargs):
        users_without_profiles = User.objects.filter(profile__isnull=True)
        for user in users_without_profiles:
            Profile.objects.create(user=user)
            self.stdout.write(f"Created profile for user: {user.username}")
        self.stdout.write("Profile backfilling completed.")