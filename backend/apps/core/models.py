from django.db import models

from backend.apps.payment_card.models import PaymentCard, GiftCard


class Buyer(models.Model):
    first_name = models.CharField(verbose_name='Nombres', max_length=180)
    last_name = models.CharField(verbose_name='Apellidos', max_length=180)
    phone = models.BigIntegerField(verbose_name='Número de telefono')
    email = models.EmailField(verbose_name='Correo')
    zip_code = models.CharField(verbose_name='Código postal', max_length=180)
    street_address = models.TextField(verbose_name='Dirección de su ubicación')
    gift_card = models.ForeignKey(to=GiftCard, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Tarjeta de regalo')
    payment_card = models.ForeignKey(to=PaymentCard, on_delete=models.CASCADE, verbose_name='Método de pago', blank=True, null=True)
    active = models.BooleanField(verbose_name='Activo', default=True)
    date_add = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'buyers'
        verbose_name = 'Comprador'
        verbose_name_plural = 'Compradores'

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
