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
        password = data['password']
        nickname = data['nickname']


        # ID validation:  8~15자 / 영문 + 대소문자만... ( 특수문자 x )
        if not re.match(r'^[A-Za-z0-9]{4,15}$', username):
            raise serializers.ValidationError(
                {"username": "ID는 최소 4글자에서 최대 15글자까지 가능하며, 영문 대소문자와 숫자만 포함해야 합니다."}
            )
        # password validation
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "비밀번호가 일치하지 않습니다."}
            )
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[~!@#$%^&*(),.?":{}|<>])[A-Za-z\d~!@#$%^&*(),.?":{}|<>]{8,15}$', password):
            raise serializers.ValidationError(
                {"password": "비밀번호는 최소 8글자에서 최대 15글자까지 가능하며, 영문 대소문자, 숫자 및 특수문자를 포함해야 합니다."}
            )
        if not re.match(r'^.{2,20}$', nickname) or re.match(r'^[ㄱ-ㅎㅏ-ㅣ]+$', nickname):
            raise serializers.ValidationError(
                {"nickname": "닉네임은 최소 2글자에서 최대 20글자까지 가능하며, 자음만으로 이루어질 수 없습니다."}
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

