from django.dispatch import Signal
from django.dispatch import receiver
from django.contrib.auth.models import User as AuthUser
from ..models import User
from ..logs.logger import userEditLog


user_edited = Signal()


@receiver(user_edited)
def log_user_edit(user, altered_fields, sender, action="Edited", **kwargs):
    log_entry = userEditLog.objects.create(
        user = user,
        altered_by = sender,
        action = f'{action} user',
        details = f'{action} fields:{altered_fields}'
    )
    log_entry.save()