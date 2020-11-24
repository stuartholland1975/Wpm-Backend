from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver

from .models import OrderDetail, OrderHeader


@receiver(pre_save, sender=OrderDetail)
def update_order_value(instance, **kwargs):
    order = OrderHeader.objects.get(work_instruction=instance.work_instruction_id)
    current_order_value = order.order_value
    if instance.id:
        current_item = OrderDetail.objects.get(pk=instance.pk)
        order.order_value = current_order_value + instance.total_payable - current_item.total_payable

    order.order_value = current_order_value + instance.total_payable
    return order.save()


@receiver(pre_delete, sender=OrderDetail)
def update_order_value_on_delete(instance, **kwargs):
    order = OrderHeader.objects.get(work_instruction=instance.work_instruction_id)
    current_order_value = order.order_value
    current_item = OrderDetail.objects.get(pk=instance.pk)
    order.order_value = current_order_value - current_item.total_payable
    return order.save()


""" @receiver(post_save, sender=Worksheet)
def update_completed_value(instance, created, **kwargs):
    item = OrderDetail.objects.get(pk=instance.item_ref_id)
    order = OrderHeader.objects.get(work_instruction=item.work_instruction_id)
    print(order)
    current_value_complete = order.value.complete
    current_value_applied = order.value_applied
    if created:
        order.value_complete = current_value_complete + instance.value_complete

    if instance.applied:
        order.value_applied = current_value_applied + instance.value_complete
    return order.save()
 """