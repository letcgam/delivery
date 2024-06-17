from django.dispatch import Signal
from django.dispatch import receiver
from ..logs.logger import productEditLog


product_created = Signal()
product_edited = Signal()


@receiver(product_created)
def create_product_log(sender, product, altered_fields, **kwargs):
    log_entry = productEditLog.objects.create(
        user = sender,
        product = product,
        action = "Created product",
        details = f"Created fields:{altered_fields}"
    )
    log_entry.save()


@receiver(product_edited)
def edit_product_log(sender, product, altered_fields, **kwargs):
    log_entry = productEditLog.objects.create(
        user = sender,
        product = product,
        action = f"Edited product",
        details = f"Edited fields:{altered_fields}"
    )
    log_entry.save()
