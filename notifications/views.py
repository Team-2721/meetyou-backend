from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from . import serializers


class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        notifications = Notification.objects.filter(user=user)

        serializer = serializers.NotificationSerializer(notifications, many=True)

        return Response({"ok": True, "data": serializer.data})


class NotificationDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        user = request.user
        try:
            notification = Notification.objects.get(pk=pk, user=user)
            notification.delete()
            return Response({"ok": True, "detail": "삭제되었습니다."})
        except:
            return Response(
                {"ok": False, "detail": "존재하지 않는 알림입니다."},
                status=status.HTTP_404_NOT_FOUND,
            )
