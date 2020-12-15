from datetime import time
from django.db.models import Sum
import rest_framework.exceptions
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework_bulk.drf3.serializers import BulkSerializerMixin, BulkListSerializer

from work_orders.models import OrderHeader, Worksheet, OrderDetail, SiteLocation

from bulk_api.models import Project, Task


class BulkMixin:
    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
            kwargs['partial'] = True

        return super().get_serializer(*args, **kwargs)


class WorksheetSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta(object):
        model = Worksheet
        list_serializer_class = BulkListSerializer
        update_lookup_field = 'id'
        fields = '__all__'


class WorksheetBulkUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worksheet
        fields = '__all__'


class SiteLocationSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta(object):
        model = SiteLocation
        list_serializer_class = BulkListSerializer
        update_lookup_field = 'id'
        fields = '__all__'


class OrderDetailSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta(object):
        model = OrderDetail
        list_serializer_class = BulkListSerializer
        fields = '__all__'


class OrderDetailBulkUpdateSerializer(serializers.ModelSerializer):
    site_location = serializers.SerializerMethodField('get_site_location')
    activity_code = serializers.SerializerMethodField('get_activity_code')
    activity_description = serializers.SerializerMethodField(
        'get_activity_description')
    worksheet_ref = serializers.SerializerMethodField('get_worksheet_ref')
    project_title = serializers.SerializerMethodField('get_project_title')
    qty_complete = serializers.SerializerMethodField('get_qty_complete')
    value_complete = serializers.SerializerMethodField('get_value_complete')
    qty_applied = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True)
    value_applied = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True)
    qty_os = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True)
    applied_value = serializers.FloatField(read_only=True)
    labour_value = serializers.FloatField(read_only=True)
    materials_value = serializers.FloatField(read_only=True)

    def get_worksheet_ref(self, obj):
        return obj.location_ref.worksheet_ref

    def get_project_title(self, obj):
        return obj.work_instruction.project_title

    def get_site_location(self, obj):
        return obj.location_ref.location_ref

    def get_activity_code(self, obj):
        return obj.activity_ref.activity_code

    def get_activity_description(self, obj):
        return obj.activity_ref.activity_description

    def get_value_complete(self, obj):
        value = obj.worksheet_set.aggregate(Sum(('value_complete')))
        return value['value_complete__sum']

    def get_qty_complete(self, obj):
        value = obj.worksheet_set.aggregate(Sum(('qty_complete')))
        return value['qty_complete__sum']

    class Meta(object):
        model = OrderDetail
        fields = '__all__'


class CurrentProjectDefault(object):
    requires_context = True

    def __call__(self, serializer_field):
        try:
            self.project = Project.objects.get(
                id=serializer_field.context["request"].parser_context["kwargs"][
                    "project_id"
                ]
            )
        except ObjectDoesNotExist:
            raise ValidationError("Project does not exist.")

        return self.project


class TaskSerializer(serializers.ModelSerializer):
    project = serializers.HiddenField(default=CurrentProjectDefault())

    def update(self, instance, validated_data):
        instance.description = validated_data["description"]
        instance.name = validated_data["name"]

        instance.save()

        return instance

    class Meta:
        model = Task
        fields = ("id", "name", "project", "description", "last_modified")
        read_only_fields = ("id", "last_modified")
