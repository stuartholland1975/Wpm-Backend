from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework_bulk import (
    BulkModelViewSet
)

from .serializers import WorksheetSerializer, OrderDetailSerializer, TaskSerializer
from work_orders.models import OrderDetail, Worksheet


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
            serializer = self.get_serializer(inst, data=data[inst.id], partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response({})


class WorksheetBulkViewSet(BulkModelViewSet):
    queryset = Worksheet.objects.all()
    serializer_class = WorksheetSerializer
    filterset_fields = ('applied', 'application_number', 'item_ref__work_instruction',)


class TaskUpdateView(generics.UpdateAPIView):
    """
    # Update the Taks
    """

    lookup_field = "id"
    serializer_class = TaskSerializer

    def get_queryset(self):

        return Task.objects.filter(
            project__id=self.kwargs["project_id"], id=self.kwargs["id"],
        )


