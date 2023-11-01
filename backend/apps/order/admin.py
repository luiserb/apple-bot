from django.contrib import admin

from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ['buyer', 'color', 'store', 'message', 'date_add']


admin.site.register(Order, OrderAdmin)