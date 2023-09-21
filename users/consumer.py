from channels.generic.websocket import AsyncWebsocketConsumer
import json


class UserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        print(self.channel_name)

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        print(text_data)
        text = json.loads(text_data)
        message = text["message"]

        if input() == "1":  # 알림 전 체크 후 전송
            await self.channel_layer.group_send(
                self.room_group_name,
                {"message": "hi yo", "type": "chat.message"},
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"messages": event["message"]}))
