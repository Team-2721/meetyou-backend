from drf_yasg import openapi


login_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "username": openapi.Schema(type=openapi.TYPE_STRING, description="아이디"),
        "password": openapi.Schema(type=openapi.TYPE_STRING, description="비밀번호"),
    },
)
