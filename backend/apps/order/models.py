from django.db import models

from backend.apps.core.models import Buyer


class Order(models.Model):
    buyer = models.ForeignKey(to=Buyer, on_delete=models.CASCADE, verbose_name='Comprador')
    color = models.CharField(verbose_name='Color', max_length=150, blank=True, null=True)
    store = models.CharField(verbose_name='Tienda', max_length=150, blank=True, null=True)
    hour = models.CharField(verbose_name='Horario', max_length=150, blank=True, null=True)
    message = models.TextField(verbose_name='Mensaje', blank=True, null=True)
    date_add = models.DateTimeField(auto_now_add=True, verbose_name='Creado el')

    class Meta:
        db_table = 'orders'
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
    
    def __str__(self):
        return '{}'.format(self.buyer)