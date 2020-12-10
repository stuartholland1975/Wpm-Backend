from django.db.models import fields
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from fieldsignals import pre_save_changed, post_save_changed
from django_q.tasks import async_task
import datetime

from .models import OrderDetail, OrderHeader, Worksheet, SiteLocation


# @receiver(pre_save, sender=OrderDetail)
# def update_order_value(instance, **kwargs):
#     order = OrderHeader.objects.get(work_instruction=instance.work_instruction_id)
#     current_order_value = order.order_value
#     if instance.id:
#         current_item = OrderDetail.objects.get(pk=instance.pk)
#         order.order_value = current_order_value + instance.total_payable - current_item.total_payable
#
#     order.order_value = current_order_value + instance.total_payable
#     return order.save()


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
        instance.iso_week = datetime.datetime.strftime(instance.date_work_done, "%V")
        instance.iso_year = datetime.datetime.strftime(instance.date_work_done, "%Y")



@receiver(post_save, sender=Worksheet)
def update_order_complete_value(instance, created, **kwargs):
    if created:
        item = OrderDetail.objects.get(pk=instance.item_ref_id)
        order = OrderHeader.objects.get(
            work_instruction=item.work_instruction_id)
        order.value_complete = order.value_complete + instance.value_complete
        order.save()


@receiver(post_save, sender=SiteLocation)
def update_worksheet_ref(instance, created, **kwargs):
    if created:
        instance.worksheet_ref = f"{instance.work_instruction_id}/{instance.id}"
        instance.save()

        


""" def update_applied_value(instance):
    print("task running")
    item = OrderDetail.objects.get(pk=instance.item_ref_id)
    order = OrderHeader.objects.get(work_instruction=item.work_instruction_id)
    order.save()
    previous_applied_value = order.tracker.previous('value_applied')
    current_applied_value = order.value_applied
    order.value_applied = current_applied_value + instance.value_complete
    print(current_applied_value)
    print(previous_applied_value)
    print(order.value_applied)
    print(instance.value_complete)
    order.save()
    print(order.value_applied)


@receiver(post_save, sender=Worksheet)
def change_applied_value(sender, instance, created, **kwargs):
    if not created:
        last_applied = instance.tracker.previous('applied')
        if instance.applied and not last_applied:
            item = OrderDetail.objects.get(pk=instance.item_ref_id)
            order = OrderHeader.objects.get(work_instruction=item.work_instruction_id)
            order.save()
            print("Applied Has Changed")
            print(order.value_applied)
            async_task(update_applied_value, instance)

 @receiver(post_save, sender=Worksheet)
def update_applied_value(instance, created, **kwargs):
    last_applied = instance.tracker.previous('applied')
    item = OrderDetail.objects.get(pk=instance.item_ref_id)
    order = OrderHeader.objects.get(
        work_instruction=item.work_instruction_id)
    current_applied_value = order.value_applied
    
    if not created and instance.applied and not last_applied:
        order.value_applied = current_applied_value + instance.value_complete
       
        print(order.value_applied)
        print(instance.value_complete)
        order.save()
        print(order.value_applied)


@receiver(pre_save, sender=Worksheet)
def update_applied_value(sender, instance,  **kwargs):
    if instance.id is None:
        pass
    else:
        item = OrderDetail.objects.get(pk=instance.item_ref_id)
        order = OrderHeader.objects.get(
        work_instruction=item.work_instruction_id)
        current_applied_value = order.value_applied
        last_applied = instance.tracker.previous('applied')
        if instance.applied and not last_applied:
            order.value_applied = current_applied_value + instance.value_complete
            print(current_applied_value)
            print(order.value_applied)
            print(instance.value_complete)
            order.save()
            print(order.value_applied)  


 @receiver(post_save_changed, sender=Worksheet)
def print_all_field_changes(sender, instance, changed_fields=None, **kwargs):
    for field, (old, new) in changed_fields.items():
        print(f"{field} changed from {old} to {new}")


@receiver(pre_save_changed, sender=Worksheet)
def print_all_field_changes(sender, instance, changed_fields=None, **kwargs):
    for field, (old, new) in changed_fields.items():
        print(f"{field} changed from {old} to {new}")
 """
 