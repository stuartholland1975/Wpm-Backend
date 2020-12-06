from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('activity', views.ActivityViewSet)
router.register('activityunit', views.ActivityUnitsViewSet)
router.register('orderheader', views.OrderHeaderViewSet)
router.register('orderdetail', views.OrderDetailViewSet)
router.register('sitelocation', views.SiteLocationViewSet)
router.register('supervisors', views.SupervisorViewSet)
router.register('worksheet', views.WorksheetViewSet)
router.register('images', views.ImageViewSet)
router.register('documents', views.DocumentViewSet)
router.register('applications', views.ApplicationViewSet)
router.register('orderstatus', views.OrderStatusViewSet)
router.register('areas', views.AreaViewSet)
router.register('worktypes', views.WorkTypesViewSet)
router.register('ratesets', views.RateSetViewSet)


urlpatterns = [
    path('api/', include(router.urls)),

    path('orders/summary/<int:work_instruction>', views.OrderSummaryInfo.as_view(), name='order-summary-info'),
    path('orders/locations/<int:work_instruction>', views.OrderLocations.as_view()),
    path('orders/work-instructions/available', views.AvailableOrderHeaders.as_view()),
    path('orders/workload/weeks', views.WorkDoneWeeks.as_view()),
    path('orders/workload', views.WorkDone.as_view()),

    path('activity/info', views.ActivityInfo.as_view(), name='activity-info'),
    path('orderdetail/item/<int:id>', views.OrderItem.as_view()),
    path('commercial/applications/orders/', views.ApplicationOrders.as_view()),
    path('commercial/applications/current', views.CurrentApplication.as_view()),
    path('commercial/application/detail/<int:app_number>', views.ApplicationInformationView.as_view()),

]
