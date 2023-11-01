from django.contrib import admin

from .models import PaymentCard, GiftCard




class PaymentCardAdmin(admin.ModelAdmin):
    list_display = ['number', 'expiration', 'cvv', 'status']


admin.site.register(PaymentCard, PaymentCardAdmin)
admin.site.register(GiftCard)