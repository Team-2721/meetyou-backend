from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import login
from channels.db import database_sync_to_async
from django.db import transaction
from django.contrib.auth.models import AnonymousUser
import json
from . import models
from .utils import date_gap_validation
from users.models import User
from notifications.models import Notification


@database_sync_to_async
def get_user(username):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return AnonymousUser()


# receive에서 다 처리하지 말고 (attendee 생성 등) connect에서 만들고 receive에서 처리하는 게 가장 깔끔함.


class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_pk = self.scope["url_route"]["kwargs"]["room_pk"]
        self.room_group_name = f"chat_{self.room_pk}"

        user = self.scope["user"]

        try:
            with transaction.atomic():
                self.room = models.Room.objects.get(pk=self.room_pk)

        except Exception as e:
            return

        if user.is_authenticated:
            self.attendee, _ = models.Attendee.objects.get_or_create(
                user=user, room=self.room
            )

            await login(
                self.scope, user
            )  # 아래 코드에서 그룹 추가하는 건 해당 사람이 알림 켰는지 확인하고 나서 group_add 실행
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        else:
            return  # 없는 경우 소켓 연결이 되지 않은 상태에서 메시지 전달하는 법

        # if user.is_authenticated:
        #     self.attendee, _ = models.Attendee.objects.get_or_create(
        #         user=user, room=room
        #     )

        #     await login(self.scope, user)  # 아래 코드에서 그룹 추가하는 건 해당 사람이 알림 켰는지 확인하고 나서
        #     await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        #     await self.accept()
        # else:
        #     return  # 없는 경우 소켓 연결이 되지 않은 상태에서 메시지 전달하는 법

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text = json.loads(text_data)
        send_type = text["send_type"]
        user = self.scope["user"]

        if send_type == "done":
            try:
                with transaction.atomic():
                    room = self.room

                    votes = models.Vote.objects.filter(attendee=self.attendee)
                    if votes:
                        votes.delete()

                    dates = text["dates"]

                    vote_dates = [
                        models.Vote(attendee=self.attendee, date=date) for date in dates
                    ]
                    models.Vote.objects.bulk_create(vote_dates)

                    self.attendee.is_completed = True
                    self.attendee.save()

                    attendees_number = models.Attendee.objects.filter(room=room).count()

                    if attendees_number == room.attendee_number:  # 알림 전 체크 후 전송
                        Notification.objects.create(
                            user=user,
                            message=f"{room.name}의 모든 투표가 완료되었습니다. 결과를 확인해 주세요!",
                        )
                        await self.channel_layer.group_send(
                            self.room_group_name,
                            {
                                "message": "모든 투표가 완료되었습니다. 결과를 확인해 주세요!",
                                "room": room.pk,
                                "type": "chat.message",
                            },
                        )
                        await self.channel_layer.group_discard(
                            self.room_group_name, self.channel_name
                        )
                    else:
                        await self.send(
                            text_data=json.dumps(
                                {"message": "투표 완료되었습니다. 다른 참가자들이 모두 투표 하면 알려드릴게요!"}
                            )
                        )

            except Exception as e:
                self.send(text_data=json.dumps({"message": e}))

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps({"message": event["message"], "room": event["room"]})
        )

    async def invalid_room(self, event):
        await self.send(
            text_data=json.dumps({"message": event["message"], "ok": event["ok"]})
        )


# class RoomConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_pk = self.scope["url_route"]["kwargs"]["room_pk"]
#         self.room_group_name = f"chat_{self.room_pk}"

#         username = self.scope["url_route"]["kwargs"]["username"]

#         user = await get_user(username)

#         if user.is_authenticated:
#             await login(self.scope, user)
#             await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#             await self.accept()
#         else:
#             return  # 없는 경우 소켓 연결이 되지 않은 상태에서 메시지 전달하는 법

#     async def disconnect(self, code):
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

#     async def receive(self, text_data):
#         text = json.loads(text_data)
#         message = text["message"]

#         user = self.scope["user"]

#         # test = Session.objects.get(pk=self.scope["session"])
#         try:
#             with transaction.atomic():
#                 room = models.Room.objects.get(pk=self.room_pk)
#         except Exception as e:
#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {"message": "존재하지 않는 방입니다.", "ok": False, "type": "invalid.room"},
#             )
#             return

#         with transaction.atomic():
#             attendee, _ = models.Attendee.objects.get_or_create(user=user, room=room)

#             attendees_number = models.Attendee.objects.filter(room=room).count()

#         if attendees_number == room.attendee_number:  # 알림 전 체크 후 전송
#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {"message": "투표가 완료되었습니다. 결과를 확인해 주세요!", "type": "chat.message"},
#             )

#     async def chat_message(self, event):
#         await self.send(text_data=json.dumps({"message": event["message"]}))

#     async def invalid_room(self, event):
#         await self.send(
#             text_data=json.dumps({"message": event["message"], "ok": event["ok"]})
#         )
