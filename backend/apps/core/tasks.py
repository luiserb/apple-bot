from celery import shared_task
from celery.schedules import crontab
from backend.celery import app

from backend.apps.core.models import Buyer
from .apple import AppleBot


@shared_task
def apple_bot():
    buyers = Buyer.objects.filter(active=True)
    if buyers.count() >= 1:
        for buyer in buyers:
            try:
                AppleBot(buyer=buyer)
            except Exception as error:
                print('Error en compra del usuario {} : {}'.format(buyer.id, error))


app.conf.beat_schedule = {
    'apple_bot': {
        'task': 'backend.apps.core.tasks.apple_bot',
        'schedule': crontab(minute='*/3'),
        'args': (),
    }
}