from django.contrib import admin
from .models import Item,Category,OrderItem,Cart


# Register your models here.
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(OrderItem)
admin.site.register(Cart)