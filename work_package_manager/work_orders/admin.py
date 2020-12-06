from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Activity, ActivityUnits, OrderHeader, OrderStatus, Area, SiteLocation, OrderDetail, Worksheet, \
    WorkType, SuperVisor, ConstructionImage, Application, Image, Post, Document, RateSetUplifts


@admin.register(Activity)
class ActivityAdmin(ImportExportModelAdmin):
    pass



@admin.register(ActivityUnits)
class ActivityUnitsAdmin(ImportExportModelAdmin):
    pass


@admin.register(Area)
class AreaAdmin(ImportExportModelAdmin):
    pass


@admin.register(OrderHeader)
class OrderHeaderAdmin(ImportExportModelAdmin):
    pass


@admin.register(OrderStatus)
class OrderStatusAdmin(ImportExportModelAdmin):
    pass


@admin.register(SiteLocation)
class SiteLocationAdmin(ImportExportModelAdmin):
    pass


@admin.register(OrderDetail)
class OrderHeaderAdmin(ImportExportModelAdmin):
    pass


@admin.register(Worksheet)
class WorksheetAdmin(ImportExportModelAdmin):
    pass


@admin.register(WorkType)
class WorkTypeAdmin(ImportExportModelAdmin):
    pass


@admin.register(SuperVisor)
class SupervisorAdmin(ImportExportModelAdmin):
    pass


@admin.register(ConstructionImage)
class ConstructionImageAdmin(ImportExportModelAdmin):
    pass


@admin.register(Application)
class ApplicationAdmin(ImportExportModelAdmin):
    pass


@admin.register(Image)
class ImageAdmin(ImportExportModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(ImportExportModelAdmin):
    pass


@admin.register(Document)
class DocumentAdmin(ImportExportModelAdmin):
    pass


@admin.register(RateSetUplifts)
class RateSetUpliftsAdmin(ImportExportModelAdmin):
    pass
