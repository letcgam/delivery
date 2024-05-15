from django.dispatch import receiver
from .signals import user_edited
from ..models import userEditLog


@receiver(user_edited)
def log_user_edit(user, edited_fields, action="Edited", sender=None, **kwargs):
    log_entry = userEditLog.objects.create(
        user = user,
        altered_by = user if not sender else sender,
        action = f'{action} user',
        details = f'{action}: {edited_fields}'
    )
    log_entry.save()