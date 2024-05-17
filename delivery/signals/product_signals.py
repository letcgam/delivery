from django.dispatch import Signal
from django.dispatch import receiver
from ..logs.logger import productEditLog


product_edited = Signal()


@receiver(product_edited)
def log_product_edit(sender, product, altered_fields, action="Edited", **kwargs):
    log_entry = productEditLog.objects.create(
        user = sender,
        product = product,
        action = f'{action} user',
        details = f'{action} fields:{altered_fields}'
    )
    log_entry.save()
