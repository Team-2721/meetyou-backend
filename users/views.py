from django.contrib.auth import login, logout, get_user_model
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from . import serializers, schemata
from .permissions import IsLogOut


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags=["내 정보 확인"], operation_id="my profile")
    def get(self, request):
        user = request.user

        serializer = serializers.MeSerializer(user, context={"request": request})

        return Response(
            {"ok": True, "data": serializer.data}, status=status.HTTP_200_OK
        )


class LoginView(APIView):
    permission_classes = [IsLogOut]

    @swagger_auto_schema(
        tags=["로그인"], request_body=schemata.login_schema, operation_id="user login"
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"ok": False, "detail": "username 혹은 password을 입력해 주세요."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user_model = get_user_model()
            user = user_model.objects.get(username=username)
            if user.check_password(password):
                login(request, user)
                return Response({"ok": True, "detail": "로그인 되었습니다."})
            else:
                # 비밀번호가 틀린 경우
                return Response(
                    {"ok": False, "detail": "잘못된 회원 정보입니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except:
            # 존재하지 않는 회원인 경우
            return Response(
                {"ok": False, "detail": "잘못된 회원 정보입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags=["로그아웃"], operation_id="user logout")
    def post(self, request):
        logout(request)
        return Response({"ok": True})
