from django.dispatch import Signal
from django.dispatch import receiver
from ..logs.logger import userEditLog


user_created = Signal()
user_edited = Signal()


@receiver(user_created)
def log_create_user(user, fields, sender, **kwargs):
    log_entry = userEditLog.objects.create(
        user = user,
        altered_by = sender,
        action = "Created user",
        details = f"Created fields:{fields}"
    )
    log_entry.save()


@receiver(user_edited)
def log_edit_user(user, altered_fields, sender, **kwargs):
    log_entry = userEditLog.objects.create(
        user = user,
        altered_by = sender,
        action = f"Edited user",
        details = f"Edited fields:{altered_fields}"
    )
    log_entry.save()