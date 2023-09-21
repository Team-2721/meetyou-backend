from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class TestView(APIView):
    task_id = openapi.Parameter(
        "task_id",
        openapi.IN_PATH,
        description="task_id path",
        required=True,
        type=openapi.TYPE_NUMBER,
    )

    @swagger_auto_schema(
        tags=["테스트입니다."],
        manual_parameters=[task_id],
    )
    def get(self, request):
        return Response({"ok": True}, status=status.HTTP_201_CREATED)
