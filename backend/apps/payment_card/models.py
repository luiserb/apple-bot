from django.db import models


class PaymentCard(models.Model):
    number = models.BigIntegerField(verbose_name='Número de tarjeta', unique=True)
    expiration = models.CharField(verbose_name='Expiración', max_length=5)
    cvv = models.CharField(verbose_name='CVV', max_length=4)
    status = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payment_cards'
        verbose_name = 'Tarjeta de pago'
        verbose_name_plural = 'Tarjetas de pagos'
    
    def __str__(self):
        return '{}'.format(self.number)


class GiftCard(models.Model):
    number = models.CharField(verbose_name='Número de tarjeta de regalo', max_length=158, unique=True)
    date_add = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'gift_cards'
        verbose_name = 'Tarjeta de regalo'
        verbose_name_plural = 'Tarjetas de regalo'
    
    def __str__(self):
        return '{}'.format(self.number)