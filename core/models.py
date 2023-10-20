from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일시")
    updated_at = models.DateTimeField(auto_now=True, editable=True, verbose_name="수정일시")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="삭제일시")

    class Meta:
        abstract = True
