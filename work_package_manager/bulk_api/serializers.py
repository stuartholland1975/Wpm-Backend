from datetime import time

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
