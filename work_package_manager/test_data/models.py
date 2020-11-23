from datetime import datetime

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from model_utils import Choices


class OrderHeader(models.Model):
    work_instruction = models.IntegerField(verbose_name='Work Instruction', unique=True)
    job_number = models.CharField(max_length=50, verbose_name='Job Number')
    project_title = models.CharField(max_length=255, verbose_name='Project Title')
    project_address = models.CharField(max_length=255, verbose_name='Address', null=True, blank=True)
    start_date = models.DateField(default=datetime.now)
    end_date = models.DateField(default=datetime.now)
    issued_date = models.DateField(default=datetime.now)
    order_value = models.DecimalField(decimal_places=2, max_digits=12, default=0.00, blank=True)
    value_complete = models.DecimalField(decimal_places=2, max_digits=12, default=0.00, blank=True)
    value_applied = models.DecimalField(decimal_places=2, max_digits=12, default=0.00, blank=True)
    notes = models.TextField(blank=True, null=True)
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


class OrderDetail(models.Model):
    ITEM_TYPES = Choices(('BOQ', 'BOQ'),
                         ('VARN', 'Variation'),
                         ('MISC', 'Misc'),
                         ('FREE', 'Free'),
                         ('DIRECTS', 'Directs'),
                         )
    work_instruction = models.ForeignKey(OrderHeader, to_field='work_instruction', on_delete=models.SET_NULL, null=True)

    item_number = models.IntegerField(verbose_name='Item Number', null=True)
    item_type = models.CharField(choices=ITEM_TYPES, default=ITEM_TYPES.BOQ, null=True, max_length=10)

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


@receiver(post_save, sender=OrderDetail)
def update_order_value(sender, instance, created, **kwargs):
    order = OrderHeader.objects.get(work_instruction=instance.work_instruction_id)
    current_order_value = order.order_value
    order.order_value = current_order_value + instance.total_payable
    return order.save()
