from django.dispatch import Signal
from django.dispatch import receiver
from ..logs.logger import orderUpdateLog
from ..models import OrderStatus


order_created = Signal()
order_edited = Signal()


@receiver(order_created)
def create_order_log(order, sender, **kwargs):
    log_entry = orderUpdateLog.objects.create(
        order = order,
        user = sender,
        action = "created",
        new_status = OrderStatus.objects.get(description = "Processing")
    )
    log_entry.save()

    
@receiver(order_edited)
def update_order_log(order, sender, old_status, new_status, **kwargs):
    log_entry = orderUpdateLog.objects.create(
        order = order,
        user = sender,
        action = "edited",
        old_status = old_status,
        new_status = new_status
    )
    log_entry.save()