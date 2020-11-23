from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import OrderHeader, OrderDetail


@admin.register(OrderHeader)
class OrderHeaderAdmin(ImportExportModelAdmin):
    pass


@admin.register(OrderDetail)
class OrderHeaderAdmin(ImportExportModelAdmin):
    pass
