from django.db.models import Sum, Count, IntegerField, Q, F
from django.db.models.functions import Coalesce, Cast
from django_filters import rest_framework as filters
from drf_multiple_model.views import ObjectMultipleModelAPIView
from rest_framework import viewsets, generics, permissions

from .models import ActivityUnits, Activity, Application, Area, OrderHeader, OrderDetail, OrderStatus, SiteLocation, \
    SuperVisor, Worksheet, WorkType, Image, Document, RateSetUplifts
from .serializers import ActivitySerializer, ActivityUnitSerializer, AreaSerializer, OrderHeaderSerializer, \
    OrderDetailSerializer, \
    SiteLocationSerializer, OrderStatusSerializer, WorkTypeSerializer, WorksheetSerializer, \
    SupervisorSerializer, \
    ImagesSerializer, DocumentSerializer, ApplicationSerializer, RateSetSerializer


class ActivityUnitsViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    queryset = ActivityUnits.objects.all()
    serializer_class = ActivityUnitSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all().order_by('id')
    serializer_class = ActivitySerializer


class OrderHeaderViewSet(viewsets.ModelViewSet):
    queryset = OrderHeader.objects.annotate(order_value=Sum('orderdetail__total_payable'),
                                            item_count=Count('orderdetail__id')).order_by('id')
    serializer_class = OrderHeaderSerializer
    filterset_fields = ('orderdetail__worksheet__application_number',)


class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.annotate(qty_complete=Coalesce(Sum('worksheet__qty_complete'), 0.00),
                                            value_complete=Coalesce(Sum('worksheet__value_complete'), 0.00),
                                            qty_applied=Coalesce(
                                                Sum('worksheet__qty_complete', filter=Q(worksheet__applied=True)),
                                                0.00),
                                            value_applied=Coalesce(
                                                Sum('worksheet__value_complete', filter=Q(worksheet__applied=True)),
                                                0.00),
                                            qty_os=F('qty_ordered') - Coalesce(Sum('worksheet__qty_complete'), 0.00))
    serializer_class = OrderDetailSerializer
    filterset_fields = (
        'work_instruction', 'worksheet__applied', 'worksheet__application_number', 'id', 'location_ref',)


class OrderItem(generics.ListAPIView):
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        item = self.kwargs['id']
        return OrderDetail.objects.filter(pk=item).annotate(qty_complete=Coalesce(Sum('worksheet__qty_complete'), 0.00),
                                                            value_complete=Coalesce(Sum('worksheet__value_complete'),
                                                                                    0.00),
                                                            qty_applied=Coalesce(Sum('worksheet__qty_complete',
                                                                                     filter=Q(worksheet__applied=True)),
                                                                                 0.00),
                                                            value_applied=Coalesce(Sum('worksheet__value_complete',
                                                                                       filter=Q(
                                                                                           worksheet__applied=True)),
                                                                                   0.00),
                                                            qty_os=F('qty_ordered') - Coalesce(
                                                                Sum('worksheet__qty_complete'), 0.00))


class SiteLocationViewSet(viewsets.ModelViewSet):
    serializer_class = SiteLocationSerializer
    queryset = SiteLocation.objects.annotate(item_count=Count('orderdetail'),
                                             total_payable=Coalesce(Sum(
                                                 'orderdetail__total_payable'), 0),
                                             items_complete=Coalesce(Sum(Cast(
                                                 'orderdetail__item_complete',
                                                 IntegerField())), 0))
    filterset_fields = ('work_instruction',)


class SupervisorViewSet(viewsets.ModelViewSet):
    serializer_class = SupervisorSerializer
    queryset = SuperVisor.objects.all()


class OrderStatusViewSet(viewsets.ModelViewSet):
    serializer_class = OrderStatusSerializer
    queryset = OrderStatus.objects.all()


class ActivityInfo(ObjectMultipleModelAPIView):
    querylist = [
        {'queryset': Activity.objects.all().order_by('id'), 'serializer_class': ActivitySerializer},
        {'queryset': ActivityUnits.objects.all(), 'serializer_class': ActivityUnitSerializer},
    ]


class OrderLocations(generics.ListAPIView):
    serializer_class = SiteLocationSerializer

    def get_queryset(self):
        work_instruction = self.kwargs['work_instruction']
        order = OrderHeader.objects.get(work_instruction=work_instruction)
        return SiteLocation.objects.filter(work_instruction=order).annotate(item_count=Count('orderdetail'),
                                                                            total_payable=Coalesce(Sum(
                                                                                'orderdetail__total_payable'), 0),
                                                                            items_complete=Coalesce(Sum(Cast(
                                                                                'orderdetail__item_complete',
                                                                                IntegerField())), 0))


class OrderSummaryInfo(ObjectMultipleModelAPIView):
    def get_querylist(request, *args, **kwargs):
        wi = request.kwargs['work_instruction']

        order = OrderHeader.objects.get(pk=wi)
        worksheet = order.sitelocation_set.all()
        querylist = [
            {'queryset': OrderHeader.objects.filter(id=order.id).annotate(order_value=Sum('orderdetail__total_payable'),
                                                                          item_count=Count('orderdetail__id')).order_by(
                'id'), 'serializer_class': OrderHeaderSerializer},
            {'queryset': order.orderdetail_set.all().annotate(
                qty_complete=Coalesce(Sum('worksheet__qty_complete'), 0.00),
                value_complete=Coalesce(Sum('worksheet__value_complete'), 0.00),
                qty_applied=Coalesce(Sum('worksheet__qty_complete', filter=Q(worksheet__applied=True)), 0.00),
                value_applied=Coalesce(Sum('worksheet__value_complete', filter=Q(worksheet__applied=True)), 0.00),
                qty_os=F('qty_ordered') - Coalesce(Sum('worksheet__qty_complete'), 0.00)
            ).order_by('item_number'),
             'serializer_class': OrderDetailSerializer},
            {'queryset': order.sitelocation_set.annotate(item_count=Count('orderdetail'),
                                                         total_payable=Coalesce(Sum(
                                                             'orderdetail__total_payable'), 0.00),
                                                         items_complete=Coalesce(Sum(Cast(
                                                             'orderdetail__item_complete',
                                                             IntegerField())), 0.00)).order_by('id'),
             'serializer_class': SiteLocationSerializer},
            {'queryset': Image.objects.filter(location__work_instruction=order.work_instruction).order_by(
                '-image_type'),
                'serializer_class': ImagesSerializer},
        ]
        return querylist


class WorksheetViewSet(viewsets.ModelViewSet):
    serializer_class = WorksheetSerializer
    queryset = Worksheet.objects.all()
    filterset_fields = ('applied', 'application_number', 'item_ref__work_instruction',)


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class ImageFilter(filters.FilterSet):
    location_in = NumberInFilter(field_name='location', lookup_expr='in')

    class Meta:
        model = Image
        fields = ['location_in', 'location', 'location__work_instruction', ]


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImagesSerializer
    queryset = Image.objects.all()
    filter_class = ImageFilter


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    queryset = Application.objects.all().order_by('-app_number')[:5].annotate(
        application_value=Sum('worksheet__value_complete'))


class AreaViewSet(viewsets.ModelViewSet):
    serializer_class = AreaSerializer
    queryset = Area.objects.all()


class WorkTypesViewSet(viewsets.ModelViewSet):
    serializer_class = WorkTypeSerializer
    queryset = WorkType.objects.all()


class RateSetViewSet(viewsets.ModelViewSet):
    serializer_class = RateSetSerializer
    queryset = RateSetUplifts.objects.all()
