from django.db import models
from core.models import TimeStampedModel


class Notification(TimeStampedModel):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="notifications"
    )
    message = models.CharField(max_length=100)
    is_read = models.BooleanField(default=False)
