from rest_framework import serializers
from .models import ActivityUnits, Activity, Application, Area, OrderHeader, OrderDetail, OrderStatus, SiteLocation, \
    SuperVisor, Worksheet, WorkType, ConstructionImage, Image, Post, Document, RateSetUplifts


class ActivityUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityUnits
        fields = ['id', 'unit_description']


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = "__all__"


class WorkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkType
        fields = "__all__"


class WorksheetSerializer(serializers.ModelSerializer):
    order_ref = serializers.SerializerMethodField('get_work_instruction')
    item_number = serializers.SerializerMethodField('get_item_number')
    location_ref = serializers.SerializerMethodField('get_location_ref')
    supervisor_name = serializers.SerializerMethodField("get_supervisor_name")

    def get_supervisor_name(self, obj):
        return f"{obj.completed_by.first_name + '  ' + obj.completed_by.surname}"

    def get_work_instruction(self, obj):
        return obj.worksheet_ref.work_instruction_id

    def get_item_number(self, obj):
        return obj.item_ref.item_number

    def get_location_ref(self, obj):
        return obj.worksheet_ref.location_ref

    class Meta:
        model = Worksheet
        fields = '__all__'


class SupervisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperVisor
        fields = '__all__'


class ActivitySerializer(serializers.ModelSerializer):
    unit_description = serializers.SerializerMethodField('get_unit_description')

    def get_unit_description(self, obj):
        return obj.unit.unit_description

    class Meta:
        model = Activity
        fields = ['id', 'activity_code', 'activity_description', 'unit', 'unit_description', 'labour_base',
                  'labour_uplift', 'labour_total', 'materials_other', 'total_payable']


class OrderHeaderSerializer(serializers.ModelSerializer):
    area_description = serializers.SerializerMethodField('get_area_description')
    work_type = serializers.SerializerMethodField('get_work_type')
    status_description = serializers.SerializerMethodField('get_status_description')
    order_value = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    item_count = serializers.IntegerField(read_only=True)
    issued_date_formatted = serializers.SerializerMethodField('format_date')

    def get_work_type(self, obj):
        return obj.project_type.work_type_description

    def get_area_description(self, obj):
        return obj.area.area_description

    def get_status_description(self, obj):
        return obj.project_status.status_description

    def format_date(self, obj):
        return obj.issued_date.strftime('%d/%m/%Y')

    class Meta:
        model = OrderHeader
        fields = '__all__'
        datatables_always_serialize = 'id'


class OrderDetailSerializer(serializers.ModelSerializer):
    site_location = serializers.SerializerMethodField('get_site_location')
    activity_code = serializers.SerializerMethodField('get_activity_code')
    activity_description = serializers.SerializerMethodField('get_activity_description')
    worksheet_ref = serializers.SerializerMethodField('get_worksheet_ref')
    project_title = serializers.SerializerMethodField('get_project_title')
    qty_complete = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    value_complete = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    qty_applied = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    value_applied = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    qty_os = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

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


class SiteLocationSerializer(serializers.ModelSerializer):
    item_count = serializers.IntegerField(read_only=True)
    items_complete = serializers.IntegerField(read_only=True)
    total_payable = serializers.FloatField(read_only=True)

    class Meta:
        model = SiteLocation
        fields = '__all__'
        datatables_always_serialize = 'id'


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
