from django.db import models
from datetime import datetime
from model_utils import Choices
from exiffield.fields import ExifField
from exiffield.getters import exifgetter


class ActivityUnits(models.Model):
    unit_description = models.CharField(max_length=25, verbose_name='Unit')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.unit_description

    def activity_unit_natural_key(self):
        return self.unit_description


class Activity(models.Model):
    activity_code = models.CharField(max_length=50, verbose_name='Activity Ref', unique=True)
    activity_description = models.CharField(max_length=255, verbose_name='Activity Description')
    unit = models.ForeignKey(ActivityUnits, on_delete=models.PROTECT, verbose_name='Unit', null=True)
    labour_base = models.DecimalField(max_digits=12, decimal_places=2, null=True, verbose_name='Fixed Contract Labour')
    labour_uplift = models.DecimalField(max_digits=12, decimal_places=2, null=True, verbose_name='Labour Uplift')
    labour_total = models.DecimalField(max_digits=12, decimal_places=2, null=True, verbose_name='Labour Total')
    materials_other = models.DecimalField(max_digits=12, decimal_places=2, null=True, verbose_name='NEMS')
    total_payable = models.DecimalField(max_digits=12, decimal_places=2, null=True,
                                        verbose_name='Total Payable')
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.activity_code


class Area(models.Model):
    area_code = models.CharField(max_length=1, verbose_name='Region Code')
    area_description = models.CharField(max_length=255, verbose_name='Region')

    def __str__(self):
        return self.area_description


class OrderStatus(models.Model):
    status_description = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.status_description


class WorkType(models.Model):
    work_type_description = models.CharField(max_length=50, null=True, verbose_name='Work Type', blank=True)

    def __str__(self):
        return self.work_type_description


class OrderHeader(models.Model):
    work_instruction = models.IntegerField(verbose_name='Work Instruction', unique=True)
    job_number = models.CharField(max_length=50, verbose_name='Job Number')
    project_title = models.CharField(max_length=255, verbose_name='Project Title')
    project_address = models.CharField(max_length=255, verbose_name='Address', null=True, blank=True)
    project_type = models.ForeignKey(WorkType, on_delete=models.PROTECT, verbose_name='Job Type', null=True, blank=True)
    project_status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT, null=True, blank=True)
    area = models.ForeignKey(Area, on_delete=models.PROTECT, verbose_name='Area')
    start_date = models.DateField(default=datetime.now)
    end_date = models.DateField(default=datetime.now)
    issued_date = models.DateField(default=datetime.now)
    notes = models.TextField(blank=True, null=True)
    document_1 = models.FileField(upload_to='documents/', null=True, blank=True, verbose_name='H&S Pack')
    document_2 = models.FileField(upload_to='documents/', null=True, blank=True, verbose_name='Field Docs')
    document_3 = models.FileField(upload_to='documents/', null=True, blank=True, verbose_name='Field Docs')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.work_instruction} / {self.project_title}"

    def start_date_pretty(self):
        return self.start_date.strftime('%d/%m/%Y')

    def end_date_pretty(self):
        return self.end_date.strftime('%d/%m/%Y')

    def issued_date_pretty(self):
        return self.issued_date.strftime('%d/%m/%Y')


class SuperVisor(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    surname = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.surname}"


class ConstructionImage(models.Model):
    IMAGE_CLASS = Choices(('PRE', 'Pre Construction Image'),
                          ('MISC', 'Misc Construction Image'),
                          ('POST', 'Post Construction Image'),
                          )
    construction_image = models.ImageField(upload_to='images/', blank=True, verbose_name='Construction Image')
    image_type = models.CharField(choices=IMAGE_CLASS, verbose_name='Image Type', max_length=10)
    date_image = models.DateField(verbose_name='Image Date', null=True, blank=True)
    notes = models.CharField(max_length=255, verbose_name='Notes', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.construction_image.name


class SiteLocation(models.Model):
    work_instruction = models.ForeignKey(OrderHeader, to_field='work_instruction', on_delete=models.PROTECT, null=True,
                                         blank=True, verbose_name='Work Instruction')
    location_ref = models.CharField(max_length=255, verbose_name='Pole Number')
    location_description = models.CharField(max_length=255, verbose_name='Description', blank=True, null=True)
    worksheet_ref = models.CharField(max_length=50, verbose_name='Worksheet Ref', null=True, blank=True, unique=True)
    construction_image = models.ManyToManyField(ConstructionImage, blank=True, verbose_name='Construction Image')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.work_instruction.work_instruction} / {self.location_ref}"

    class Meta:
        unique_together = [['work_instruction', 'location_ref']]


class OrderDetail(models.Model):
    ITEM_TYPES = Choices(('BOQ', 'BOQ'),
                         ('VARN', 'Variation'),
                         ('MISC', 'Misc'),
                         )
    work_instruction = models.ForeignKey(OrderHeader, to_field='work_instruction', on_delete=models.SET_NULL, null=True)
    location_ref = models.ForeignKey(SiteLocation, on_delete=models.PROTECT,
                                     verbose_name='Pole Number', null=True)
    item_number = models.IntegerField(verbose_name='Item Number', null=True)
    item_type = models.CharField(choices=ITEM_TYPES, default=ITEM_TYPES.BOQ, null=True, max_length=10)
    activity_ref = models.ForeignKey(Activity, on_delete=models.PROTECT)
    qty_ordered = models.DecimalField(decimal_places=4, max_digits=12, verbose_name='Qty', default=1, null=True,
                                      blank=True)
    labour_base = models.DecimalField(decimal_places=4, max_digits=12, default=0, null=True, )
    labour_uplift = models.DecimalField(decimal_places=4, max_digits=12, default=0, null=True, )
    labour_total = models.DecimalField(decimal_places=4, max_digits=12, default=0, null=True, )
    unit_labour_payable = models.DecimalField(decimal_places=4, max_digits=12, default=0, null=True,
                                              verbose_name='Unit Labour Payable')

    materials_base = models.DecimalField(decimal_places=4, max_digits=12, default=0, null=True)
    materials_uplift = models.DecimalField(decimal_places=4, max_digits=12, default=0, null=True, )
    materials_total_excl_other_materials = models.DecimalField(decimal_places=4, max_digits=12, default=0,
                                                               null=True, verbose_name='Material Pack Total')
    materials_other = models.DecimalField(decimal_places=4, max_digits=12, default=0, null=True)
    materials_total_incl_other_materials = models.DecimalField(decimal_places=4, max_digits=12, default=0,
                                                               null=True)
    unit_materials_payable = models.DecimalField(decimal_places=4, max_digits=12, default=0, null=True,
                                                 verbose_name='Unit Materials Payable')
    total_payable = models.DecimalField(decimal_places=4, max_digits=12, default=0, null=True)
    unit_total_payable = models.DecimalField(decimal_places=4, max_digits=12, default=0, null=True,
                                             verbose_name='Unit Total Payable')
    pack_number = models.CharField(max_length=255, null=True, blank=True)
    item_status = models.CharField(max_length=20, verbose_name='Item Status', default='Open')
    item_complete = models.BooleanField(verbose_name='Item Complete', default=False, )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        unique_together = ('work_instruction', 'item_number',)

    def __str__(self):
        return f"{self.work_instruction} / {self.item_number}"


class Application(models.Model):
    app_number = models.SmallIntegerField(unique=True, verbose_name='Application No')
    app_date = models.DateField(verbose_name='Application Date')
    app_ref = models.CharField(max_length=255, verbose_name='Application Ref')
    app_open = models.BooleanField(verbose_name='Application Open')
    app_current = models.BooleanField(verbose_name='Current Application')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.app_ref

    def app_date_pretty(self):
        return self.app_date.strftime('%d/%m/%Y')


class Worksheet(models.Model):
    worksheet_ref = models.ForeignKey(SiteLocation, on_delete=models.PROTECT,
                                      verbose_name='Location Ref')
    item_ref = models.ForeignKey(OrderDetail, on_delete=models.PROTECT, verbose_name='Item', null=True, blank=True)
    date_work_done = models.DateField(verbose_name='Work Done Date', null=True, blank=True)
    qty_complete = models.DecimalField(verbose_name='Qty Complete', max_digits=10, decimal_places=4, null=True,
                                       blank=True)
    value_complete = models.DecimalField(verbose_name='Value Complete', max_digits=10, decimal_places=4, null=True,
                                         blank=True)
    materials_complete = models.DecimalField(verbose_name='Materials Complete', max_digits=10, decimal_places=4,
                                             null=True,
                                             blank=True)
    labour_complete = models.DecimalField(verbose_name='Labour Complete', max_digits=10, decimal_places=4,
                                          null=True,
                                          blank=True)
    completed_by = models.ForeignKey(SuperVisor, on_delete=models.PROTECT, verbose_name='Supervisor', null=True)
    applied = models.BooleanField(verbose_name='Applied For', default=False)

    application_number = models.ForeignKey(Application, to_field='app_number', on_delete=models.PROTECT, null=True,
                                           blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def work_done_date_pretty(self):
        return self.date_work_done.strftime('%d/%m/%Y')

    def __str__(self):
        return f"{self.worksheet_ref}"


class Image(models.Model):
    IMAGE_CLASS = Choices(('PRE', 'Pre Construction Image'),
                          ('MISC', 'Misc Construction Image'),
                          ('POST', 'Post Construction Image'),
                          )
    title = models.CharField(max_length=255, verbose_name='Title', null=True, blank=False)
    location = models.ForeignKey(SiteLocation, on_delete=models.PROTECT, verbose_name='Site Location')
    construction_image = models.ImageField(upload_to='images/original', blank=True, verbose_name='Construction Image')
    construction_image_resized = models.ImageField(upload_to='images/resized/', blank=True,
                                                   verbose_name='Resized Construction Image')
    image_type = models.CharField(choices=IMAGE_CLASS, verbose_name='Image Type', max_length=10)
    date_image = models.DateField(verbose_name='Image Date', null=True, blank=True)
    notes = models.CharField(max_length=255, verbose_name='Notes', null=True, blank=True)
    camera = models.CharField(editable=False, max_length=100, null=True, blank=True)
    gps_lat = models.CharField(editable=False, max_length=100, null=True, blank=True)
    gps_long = models.CharField(editable=False, max_length=100, null=True, blank=True)
    gps_date = models.CharField(editable=False, max_length=100, null=True, blank=True)
    date_time_original = models.CharField(editable=False, max_length=100, null=True, blank=True)
    exif = ExifField(source='construction_image',
                     denormalized_fields={'camera': exifgetter('Model'), 'gps_lat': exifgetter('GPSLatitude'),
                                          'gps_long': exifgetter('GPSLongitude'),
                                          'gps_date': exifgetter('GPSDateTime'),
                                          'date_time_original': exifgetter('DateTimeOriginal'), }, )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.construction_image.name


class Post(models.Model):
    IMAGE_CLASS = Choices(('PRE', 'Pre Construction Image'),
                          ('MISC', 'Misc Construction Image'),
                          ('POST', 'Post Construction Image'),
                          )
    title = models.CharField(max_length=100)
    content = models.TextField()
    image_type = models.CharField(choices=IMAGE_CLASS, verbose_name='Image Type', max_length=10)
    construction_image = models.ImageField(upload_to='images/', blank=True, verbose_name='Construction Image')
    date_image = models.DateField(verbose_name='Image Date', null=True, blank=True)
    location = models.ForeignKey(SiteLocation, on_delete=models.PROTECT, verbose_name='Site Location')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title


class Document(models.Model):
    work_instruction = models.ForeignKey(OrderHeader, on_delete=models.PROTECT)
    document = models.FileField(upload_to='documents/', null=True, blank=True)
    document_title = models.CharField(max_length=100)

    def __str__(self):
        return self.document_title


class RateSetUplifts(models.Model):
    rateset_code = models.IntegerField(unique=True, verbose_name="Rate Set Code")
    labour_uplift_percentage = models.DecimalField(max_digits=5, decimal_places=4,
                                                   verbose_name="Labour Percentage Uplift")
    materials_uplift_percentage = models.DecimalField(max_digits=5, decimal_places=4,
                                                      verbose_name="Materials Percentage Uplift")
    date_from = models.DateField(verbose_name="Date Applicable From")
    date_to = models.DateField(verbose_name="Date Applicable To")
