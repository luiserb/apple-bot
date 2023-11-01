from django.contrib import admin

from .models import Buyer


class BuyerAdmin(admin.ModelAdmin):
    def metodo_de_pago(self):
        if self.gift_card:
            return 'Tarjeta Regalo'
        elif self.payment_card:
            return 'Tarjeta de débito'
        else:
            return 'Ninguno'
    
    list_display = ['first_name', 'last_name', 'zip_code', metodo_de_pago]


admin.site.register(Buyer, BuyerAdmin)