from django.core.management.base import BaseCommand

from backend.apps.core.models import Buyer
from backend.apps.core.apple import AppleBot


class Command(BaseCommand):
    help:str = 'Apple Bot'

    def handle(self, *args, **options) -> None:
        buyers = Buyer.objects.filter(active=True)
        if buyers.count() >= 1:
            for buyer in buyers:
                AppleBot(buyer=buyer)