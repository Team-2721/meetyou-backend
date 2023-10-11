from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password # 패스워드 검중도구
from rest_framework import serializers
import re


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "nickname",
            "avatar",
        )

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'nickname')

    def validate(self, data):
        username = data['username']
        
        # ID validation: at least 8 characters long and must include a special character or number and a letter
        if len(username) < 8 or not re.search('[A-Za-z]', username) or not re.search('[0-9!@#$%^&*(),.?":{}|<>]', username):
            raise serializers.ValidationError(
                {"username": "ID 는 최소 8 글자이상이여야 하고, 특수문자나 숫자를 포함해야 합니다."}
            )

        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            nickname=validated_data['nickname'],
        )
        
        user.set_password(validated_data['password'])
        user.save()

        return user

#비밀번호 검증식 잘 타는지 예시
# {
# "username": "bobo2",
# "password": "1234",
# "password2": "1234",
# "nickname": "nickname"
# }

#아이디 검증식 잘 타는지 예시
#  {
#  "username": "1",
#  "password": "dkssud!!",
#  "password2": "dkssud!!",
#  "nickname": "nickname"
#  }