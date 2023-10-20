from rest_framework import status
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import F, Case, When, Subquery, OuterRef, Value, Count, Exists, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import serializers, models
from core.utils import now_minus_hour_result, get_room_code


class RoomSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        code = request.query_params.get("code", None)

        if not code:
            return Response(
                {"ok": False, "detail": "방 코드가 입력되지 않았습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            room_code = models.RoomCode.objects.get(code=code)
            room = room_code.room
            attendees = models.Attendee.objects.filter(room=room).count()
            if (
                room_code.room.created_at <= now_minus_hour_result(12)
                or room.attendee_number <= attendees
            ):
                room_code.delete()
                return Response(
                    {"ok": False, "detail": "투표가 끝난 방입니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                attendee, _ = models.Attendee.objects.get_or_create(
                    room=room, user=request.user
                )
                serializer = serializers.RoomSerializer(
                    room, context={"request": request}
                )
                return Response({"ok": True, "data": serializer.data})
        except Exception as e:
            return Response(
                {"ok": False, "detail": "유효하지 않는 코드입니다."},
                status=status.HTTP_404_NOT_FOUND,
            )


class RoomListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        page = request.query_params.get("page", 1)
        page_size = request.query_params.get("page_size", 10)

        attendees_subquery = (
            models.Attendee.objects.filter(room=OuterRef("room"))
            .annotate(cnt=Count("pk"))
            .values("cnt")
        )

        attended_rooms = (
            models.Attendee.objects.select_related("room")
            .prefetch_related("room__code")
            .annotate(
                status=Case(
                    When(
                        Q(room__created_at__lte=now_minus_hour_result(12)),
                        then=Value("투표끝"),
                    ),
                    When(Q(is_completed=False), then=Value("투표전")),
                    When(
                        room__attendee_number__gt=attendees_subquery, then=Value("투표중")
                    ),
                    When(
                        room__attendee_number__in=attendees_subquery, then=Value("투표끝")
                    ),
                )
            )
            .filter(user=user, deleted_at__isnull=True)
            .order_by("status")
        )

        try:
            paginator = Paginator(attended_rooms, page_size)
            result = paginator.page(page)
            serializer = serializers.AttendedRoomListSerializer(result, many=True)

            return Response(
                {
                    "ok": True,
                    "data": {
                        "results": serializer.data,
                        "count": result.paginator.count,
                        "next": result.has_next(),
                        "previous": result.has_previous(),
                    },
                }
            )
        except Exception as e:
            return Response(
                {"ok": False, "detail": f"Server got Error ({e})"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        user = request.user
        data = request.data.copy()
        data["manager"] = user.pk

        serializer = serializers.RoomSerializer(data=data)

        if serializer.is_valid():
            room = serializer.save()
            models.Attendee.objects.create(room=room, user=user)
            for _ in range(10000):
                try:
                    models.RoomCode.objects.create(room=room, code=get_room_code())
                    break
                except:
                    pass
            return Response(
                {"ok": True, "detail": "방이 생성되었습니다."}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"ok": False, "detail": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RoomDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):  # 방이 투표 가능 시간이면 투표할 수 있게, 아니면 결과를 보여주게
        try:
            room = models.Room.objects.get(pk=pk)
        except:
            return Response(
                {"ok": False, "detail": "존재하지 않는 방입니다."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = serializers.RoomDetailSerializer(
            room, context={"request": request}
        )

        return Response({"ok": True, "data": serializer.data})

    def delete(self, request, pk):
        try:
            attended_room = models.Attendee.objects.get(user=request.user, room=pk)
        except Exception as e:
            return Response(
                {"ok": False, "detail": "존재하지 않는 방입니다."},
                status=status.HTTP_404_NOT_FOUND,
            )
        if not attended_room.deleted_at:
            attended_room.deleted_at = timezone.now()
            attended_room.save()

            return Response(
                {"ok": True, "detail": "삭제 되었습니다."}, status=status.HTTP_202_ACCEPTED
            )
        else:
            return Response(
                {"ok": False, "detail": "비정상적인 접근입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )


# 방 생성은 data를 빼도 됨.
# 다른 검은 체크 박스는 api 문서 최신화 필요
