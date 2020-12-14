from django.db.models import fields
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from fieldsignals import pre_save_changed, post_save_changed
from django_q.tasks import async_task
import datetime

from .models import Application, OrderDetail, OrderHeader, SuperVisor, Worksheet, SiteLocation


@receiver(post_save, sender=OrderDetail)
def update_order_value(instance, created, **kwargs):
    order = OrderHeader.objects.get(
        work_instruction=instance.work_instruction_id)
    print(order.tracker.previous('order_value'))
    if created:
        order.order_value = order.order_value + instance.total_payable
        order.save()


@receiver(pre_delete, sender=OrderDetail)
def update_order_value_on_delete(instance, **kwargs):
    order = OrderHeader.objects.get(
        work_instruction=instance.work_instruction_id)
    current_order_value = order.order_value
    current_item = OrderDetail.objects.get(pk=instance.pk)
    order.order_value = current_order_value - current_item.total_payable
    return order.save()


@receiver(pre_save, sender=Worksheet)
def update_iso_info(instance, **kwargs):
    if not instance.id:
        instance.iso_week = datetime.datetime.strftime(
            instance.date_work_done, "%V")
        instance.iso_year = datetime.datetime.strftime(
            instance.date_work_done, "%G")
        instance.iso_date = datetime.datetime.strftime(
            instance.date_work_done, "%G-W%V")


@receiver(post_save, sender=Worksheet)
def update_order_complete_value(instance, created, **kwargs):
    if created:
        item = OrderDetail.objects.get(pk=instance.item_ref_id)
        order = OrderHeader.objects.get(work_instruction=item.work_instruction_id)
        order.value_complete = order.value_complete + instance.value_complete
        order.save()


@receiver(post_save, sender=SiteLocation)
def update_worksheet_ref(instance, created, **kwargs):
    if created:
        instance.worksheet_ref = f"{instance.work_instruction_id}/{instance.id}"
        instance.save()

@receiver(post_save, sender=SuperVisor)
def update_full_name(instance, created, **kwargs):
    if created:
        instance.full_name = f"{instance.first_name} {instance.middle_name} {instance.surname}"
        instance.save()
