from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from .permissions import IsLogOut
from .serializers import RegisterSerializer

# 회원가입


class RegisterUserView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#id중복확인
class CheckUsernameView(APIView):
    def post(self, request):
        username = request.data.get('username')
        if username is None:
            return Response({"ok": False, "detail": "username을 입력해 주세요."},
                            status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"ok": False, "detail": "이미 사용 중인 ID입니다."},
                            status=status.HTTP_409_CONFLICT)
        else:
            return Response({"ok": True, "detail": "사용 가능한 ID입니다."},
                            status=status.HTTP_200_OK)
        
class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        serializer = serializers.MeSerializer(user, context={"request": request})

        return Response(
            {"ok": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    # 수정
    def patch(self, request):
        user = request.user
        serializer = serializers.MeSerializer(user, data=request.data, partial=True)
        # serializer = MeSerializer(user, data=request.data, partial=True)  # partial=True to update a data partially

        if serializer.is_valid():
            serializer.save()
            return Response({"ok": True, "data": serializer.data})

        return Response(
            {"ok": False, "detail": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # 삭제
    def delete(self, request):
        user = request.user
        user.delete()

        return Response({"ok": True}, status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = [IsLogOut]

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

    def post(self, request):
        logout(request)
        return Response({"ok": True})


class UpdateMeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # 수정
    def patch(self, request):
        user = request.user
        serializer = serializers.MeSerializer(user, data=request.data, partial=True)
        # serializer = MeSerializer(user, data=request.data, partial=True)  # partial=True to update a data partially

        if serializer.is_valid():
            serializer.save()
            return Response({"ok": True, "data": serializer.data})

        return Response(
            {"ok": False, "detail": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # 삭제
    def delete(self, request):
        user = request.user
        user.delete()

        return Response({"ok": True}, status=status.HTTP_200_OK)
