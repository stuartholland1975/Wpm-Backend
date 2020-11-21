from django.conf.urls import url
from django.urls import path, include
from rest_framework_bulk.routes import BulkRouter

from . import views

router = BulkRouter()
router.register('bulk-worksheets', views.WorksheetBulkViewSet)
# router.register('bulk-items', views.OrderDetailBulkViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('bulk-items', views.OrderDetailBulkViewSet.as_view({'patch': 'list'})),


]
