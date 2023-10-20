from django.db import models
from core.models import TimeStampedModel


class Room(TimeStampedModel):
    manager = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="rooms", verbose_name="방장"
    )
    name = models.CharField(max_length=20, verbose_name="제목")
    attendee_number = models.PositiveSmallIntegerField(verbose_name="참여 인원")
    start_date = models.DateField(verbose_name="시작 날짜")
    end_date = models.DateField(verbose_name="마감 날짜")
    comment = models.TextField(verbose_name="메모")

    class Meta:
        verbose_name_plural = "방 목록"

    def __str__(self):
        return self.name


class RoomCode(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="code")
    code = models.CharField(max_length=4, unique=True)


class Attendee(TimeStampedModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="attendees")
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False, verbose_name="투표완료여부")

    class Meta:
        verbose_name_plural = "참가자 목록"

    def __str__(self):
        return f"방[{self.room.name}]의 참가자 [{self.user.nickname}]"


class Vote(models.Model):
    attendee = models.ForeignKey(
        Attendee, on_delete=models.CASCADE, related_name="votes"
    )
    date = models.DateField(blank=False, null=False, verbose_name="날짜")

    class Meta:
        verbose_name_plural = "투표 목록"
