from django.db.models import Count, F
from rest_framework import serializers
from . import models
from core.utils import now_minus_hour_result


class AttendeeInfoSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(source="user.pk")
    nickname = serializers.CharField(source="user.nickname")
    avatar = serializers.ImageField(source="user.avatar")

    class Meta:
        model = models.Attendee
        fields = ("pk", "nickname", "avatar")


class RoomSerializer(serializers.ModelSerializer):
    attendees = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Room
        fields = (
            "pk",
            "name",
            "attendee_number",
            "start_date",
            "end_date",
            "comment",
            "attendees",
        )

    def get_attendees(self, obj):
        attendees = obj.attendees.select_related("user").all()

        serializer = AttendeeInfoSerializer(
            attendees, many=True, context={"request": self.context.get("request")}
        )
        return serializer.data


class RoomDetailSerializer(RoomSerializer):
    results = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Room
        fields = RoomSerializer.Meta.fields + ("results",)

    def get_results(self, obj):
        if obj.created_at >= now_minus_hour_result(12):
            return []
        try:
            room_code = models.RoomCode.objects.get(room=obj)
            room_code.delete()
        except:
            pass
        votes = (
            models.Vote.objects.filter(attendee__room=obj)
            .values("date")
            .annotate(cnt=Count("date"))
            .order_by("-cnt", "date")
        )
        result = [vote["date"].strftime("%Y.%m.%d") for vote in votes]
        return result[:3]


class AttendedRoomListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="room.name")
    attendee_number = serializers.IntegerField(source="room.attendee_number")
    date = serializers.SerializerMethodField(read_only=True)
    pk = serializers.IntegerField(source="room.pk")
    status = serializers.CharField()
    code = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Attendee
        fields = ("pk", "name", "attendee_number", "date", "status", "code")

    def get_date(self, obj):
        start_date = obj.room.start_date
        end_date = obj.room.end_date

        if start_date.year == end_date.year:
            return f"{start_date.strftime('%Y.%m.%d')} - {end_date.strftime('%m.%d')}"
        else:
            return (
                f"{start_date.strftime('%Y.%m.%d')} - {end_date.strftime('%Y.%m.%d')}"
            )

    def get_code(self, obj):
        code = obj.room.code.all()
        if code:
            code = code[0]

            if obj.room.created_at <= now_minus_hour_result(12):
                code.delete()
                return None
            else:
                return code.code
        else:
            return None
