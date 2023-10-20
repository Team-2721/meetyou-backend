from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from . import models


class NotificationSerializer(serializers.ModelSerializer):
    created = serializers.SerializerMethodField()
    room_pk = serializers.IntegerField(source="room.pk")

    class Meta:
        model = models.Notification
        fields = ("pk", "message", "created", "room_pk")

    def get_created(self, obj):
        now = timezone.localtime(timezone.now())
        gap = now - obj.created_at
        if gap < timedelta(minutes=1):
            return "방금 전"
        elif gap < timedelta(hours=1):
            return str(int(gap.seconds / 60)) + "분 전"
        elif gap < timedelta(days=1):
            return str(int(gap.seconds / 3600)) + "시간 전"
        elif gap < timedelta(days=7):
            date_gap = now.date() - obj.created_at.date()
            return str(date_gap.days) + "일 전"
        else:
            return obj.created_at.strftime("%Y년 %m월 %d일")
