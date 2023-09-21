from django.urls import re_path


from . import consumer

websocket_urlpatterns = [
    re_path(r"ws/test/(?P<room_name>\w+)/$", consumer.UserConsumer.as_asgi()),
]
