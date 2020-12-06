import calendar
import datetime

from django.db.models import Count
from rest_framework import serializers
from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
)

from .models import ActivityUnits, Activity, Application, Area, OrderHeader, OrderDetail, OrderStatus, SiteLocation, \
    SuperVisor, Worksheet, WorkType, Image, Document, RateSetUplifts


class ActivityUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityUnits
        fields = ['id', 'unit_description']


class AreaSerializer(serializers.ModelSerializer):
    order_value = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True)
    applied_value = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True)
    complete_value = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Area
        fields = "__all__"


class WorkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkType
        fields = "__all__"


def week_of_month(date):
    """Determines the week (number) of the month"""

    # Calendar object. 6 = Start on Sunday, 0 = Start on Monday
    cal_object = calendar.Calendar(6)
    month_calendar_dates = cal_object.itermonthdates(date.year, date.month)

    day_of_week = 1
    week_number = 1

    for day in month_calendar_dates:
        # add a week and reset day of week
        if day_of_week > 7:
            week_number += 1
            day_of_week = 1

        if date == day:
            break
        else:
            day_of_week += 1

    return week_number


class WorksheetSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    order_ref = serializers.SerializerMethodField('get_work_instruction')
    item_number = serializers.SerializerMethodField('get_item_number')
    location_ref = serializers.SerializerMethodField('get_location_ref')
    supervisor_name = serializers.SerializerMethodField("get_supervisor_name")
    week_number = serializers.SerializerMethodField("get_week_ref")
    week_of_month = serializers.SerializerMethodField('get_week_month_ref')
    work_type = serializers.SerializerMethodField('get_work_type')
    area_description = serializers.SerializerMethodField('get_area_description')
    area = serializers.SerializerMethodField('get_area')

    def get_supervisor_name(self, obj):
        return f"{obj.completed_by.first_name + '  ' + obj.completed_by.surname}"

    def get_work_instruction(self, obj):
        return obj.worksheet_ref.work_instruction_id

    def get_item_number(self, obj):
        return obj.item_ref.item_number

    def get_location_ref(self, obj):
        return obj.worksheet_ref.location_ref

    def get_week_ref(self, obj):
        return datetime.datetime.strftime(obj.date_work_done, "%W")

    def get_week_month_ref(self, obj):
        return obj.date_work_done.isocalendar()[1] - obj.date_work_done.replace(day=1).isocalendar()[1] + 1

    def get_area(self, obj):
        return obj.worksheet_ref.work_instruction.area_id

    def get_area_description(self, obj):
        return obj.worksheet_ref.work_instruction.area.area_description

    def get_work_type(self, obj):
        return obj.worksheet_ref.work_instruction.project_type.work_type_description

    class Meta:
        model = Worksheet
        list_serializer_class = BulkListSerializer
        fields = '__all__'


class SupervisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperVisor
        fields = '__all__'


class ActivitySerializer(serializers.ModelSerializer):
    unit_description = serializers.SerializerMethodField(
        'get_unit_description')

    def get_unit_description(self, obj):
        return obj.unit.unit_description

    class Meta:
        model = Activity
        fields = ['id', 'activity_code', 'activity_description', 'unit', 'unit_description', 'labour_base',
                  'labour_uplift', 'labour_total', 'materials_other', 'total_payable']


class OrderHeaderSerializer(serializers.ModelSerializer):
    area_description = serializers.SerializerMethodField(
        'get_area_description')
    work_type = serializers.SerializerMethodField('get_work_type')
    status_description = serializers.SerializerMethodField(
        'get_status_description')
    # order_value = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    item_count = serializers.IntegerField(read_only=True)
    issued_date_formatted = serializers.SerializerMethodField('format_date')
    doc_count = serializers.IntegerField(read_only=True)
    applied_value = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True)
    labour_value = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True)
    materials_value = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True)
    document_count = serializers.SerializerMethodField('get_document_count')

    def get_work_type(self, obj):
        return obj.project_type.work_type_description

    def get_area_description(self, obj):
        return obj.area.area_description

    def get_status_description(self, obj):
        return obj.project_status.status_description

    def format_date(self, obj):
        return obj.issued_date.strftime('%d/%m/%Y')

    def get_document_count(self, obj):
        return Document.objects.filter(work_instruction=obj.id).aggregate(document_count=Count('id'))

    class Meta:
        model = OrderHeader
        fields = '__all__'
        datatables_always_serialize = 'id'


class OrderDetailSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    site_location = serializers.SerializerMethodField('get_site_location')
    activity_code = serializers.SerializerMethodField('get_activity_code')
    activity_description = serializers.SerializerMethodField(
        'get_activity_description')
    worksheet_ref = serializers.SerializerMethodField('get_worksheet_ref')
    project_title = serializers.SerializerMethodField('get_project_title')
    qty_complete = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True)
    value_complete = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True)
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

    class Meta:
        model = OrderDetail
        fields = '__all__'
        datatables_always_serialize = 'id'
        list_serializer_class = BulkListSerializer


class SiteLocationSerializer(serializers.ModelSerializer):
    item_count = serializers.IntegerField(read_only=True)
    items_complete = serializers.IntegerField(read_only=True)
    total_payable = serializers.FloatField(read_only=True)
    applied_value = serializers.FloatField(read_only=True)
    labour_value = serializers.FloatField(read_only=True)
    materials_value = serializers.FloatField(read_only=True)

    class Meta:
        model = SiteLocation
        fields = '__all__'
        datatables_always_serialize = 'id'
        list_serializer_class = BulkListSerializer


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = '__all__'


class ImagesSerializer(serializers.ModelSerializer):
    site_location = serializers.SerializerMethodField('get_site_location')

    def get_site_location(self, obj):
        return obj.location.location_ref

    class Meta:
        model = Image
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    application_value = serializers.FloatField(read_only=True)

    class Meta:
        model = Application
        fields = '__all__'


class RateSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = RateSetUplifts
        fields = '__all__'
