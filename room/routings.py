from django.urls import re_path


from . import consumer

websocket_urlpatterns = [
    re_path(r"ws/room/(?P<room_pk>\w+)/$", consumer.RoomConsumer.as_asgi()),
    # re_path(
    #     r"ws/room/(?P<room_pk>\w+)/(?P<username>\w+)/$", consumer.RoomConsumer.as_asgi()
    # ),
]
