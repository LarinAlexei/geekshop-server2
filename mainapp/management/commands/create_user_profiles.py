from django.core.management import BaseCommand
from mainapp.utils import get_or_create
from authapp.models import ShopUser, ShopUserProfile


class Command(BaseCommand):
    help = "Create user profiles"

    def handle(self, *args, **options):
        for user in ShopUser.objects.all():
            get_or_create(ShopUserProfile, user=user)
