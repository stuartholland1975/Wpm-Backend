from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework_bulk import (
    BulkModelViewSet
)
from rest_framework.response import Response
from .serializers import SiteLocationSerializer, WorksheetSerializer, OrderDetailSerializer, TaskSerializer,  WorksheetBulkUpdateSerializer
from work_orders.models import OrderDetail, Worksheet, SiteLocation


class BulkMixin:
    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
            kwargs['partial'] = True

        return super().get_serializer(*args, **kwargs)


class OrderDetailBulkViewSet(BulkMixin, viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer

    @action(methods=['patch'], detail=False)
    def bulk_update(self, request):
        data = {  # we need to separate out the id from the data
            i['id']: {k: v for k, v in i.items() if k != 'id'}
            for i in request.data
        }

        for inst in self.get_queryset().filter(id__in=data.keys()):
            serializer = self.get_serializer(
                inst, data=data[inst.id], partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response({})


class WorksheetBulkViewSet(BulkModelViewSet):
    queryset = Worksheet.objects.all()
    serializer_class = WorksheetSerializer
    filterset_fields = ('applied', 'application_number',
                        'item_ref__work_instruction',)


class SiteLocationBulkViewSet(BulkModelViewSet):
    queryset = SiteLocation.objects.all()
    serializer_class = SiteLocationSerializer


class OrderDetailBulkViewSet(BulkModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer


class WorksheetBulkUpdateView(APIView):

    def get_object(self, obj_id):
        try:
            return Worksheet.objects.get(id=obj_id)
        except (Worksheet.DoesNotExist, ValidationError):
            raise status.HTTP_400_BAD_REQUEST

    def validate_ids(self, id_list):
        for id in id_list:
            try:
                Worksheet.objects.get(id=id)
            except (Worksheet.DoesNotExist, ValidationError):
                raise status.HTTP_400_BAD_REQUEST
        return True

    def put(self, request, *args, **kwargs):
        data = request.data
        worksheet_ids = [i['id'] for i in data]
        self.validate_ids(worksheet_ids)
        instances = []
        for temp_dict in data:
            worksheet_id = temp_dict['id']
            completed_by_id = temp_dict['completed_by']
            worksheet_ref_id = temp_dict['worksheet_ref']

            item_ref_id = temp_dict['item_ref']
            date_work_done = temp_dict['date_work_done']
            qty_complete = temp_dict['qty_complete']
            value_complete = temp_dict['value_complete']
            materials_complete = temp_dict['materials_complete']
            labour_complete = temp_dict['labour_complete']
            application_number_id = temp_dict['application_number']
            applied = temp_dict['applied']
            obj = self.get_object(worksheet_id)
            obj.completed_by_id = completed_by_id
            obj.worksheet_ref_id = worksheet_ref_id
            obj.item_ref_id = item_ref_id
            obj.date_work_done = date_work_done
            obj.qty_complete = qty_complete
            obj.value_complete = value_complete
            obj.materials_complete = materials_complete
            obj.labour_complete = labour_complete
            obj.application_number_id = application_number_id
            obj.applied = applied
            obj.save()
            instances.append(obj)
        serializer = WorksheetBulkUpdateSerializer(instances, many=True)
        return Response(serializer.data)
