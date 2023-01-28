from datetime import datetime, timezone
from django.contrib.auth.models import User
from django.core.exceptions import BadRequest
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from chat.models import Chatroom, Message, UserMessage
from chat.serializers import (MessageSerializer, ChatroomSerializer,
                              UserSerializer)
from chat.permissions import (ChatroomMemberOrAdmin, MemberOrAdmin, SelfOrAdmin)
from chat.viewsets import CreateListViewSet


class UserViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows users to be viewed or edited.
  """
  queryset = User.objects.all().order_by('-date_joined')
  serializer_class = UserSerializer

  permission_classes = [SelfOrAdmin]


class MessageViewSet(CreateListViewSet):
  """
  API endpoint that allows chat messages to be viewed or edited.
  """
  serializer_class = MessageSerializer

  permission_classes = [ChatroomMemberOrAdmin]

  def get_queryset(self):
    chatroom_id = self.request.query_params.get('chatroom_id')

    if chatroom_id is None:
      raise BadRequest()

    queryset = Message.objects.filter(
        chatroom__id=chatroom_id).order_by('-sent_at')
    return queryset

  @action(detail=True, methods=['post'], url_path='mark-seen')
  def mark_as_seen(self, request, pk: int):
    user: User = request.user
    message: Message = self.get_object()
    earlier_messages = Message.objects.filter(sent_at__lte=message.sent_at)
    for earlier_message in earlier_messages:
      if not UserMessage.objects.filter(
          user=user, message=earlier_message).exists():
        UserMessage.objects.create(
            user=user,
            message=earlier_message,
            seen_at=datetime.now(timezone.utc))

    return Response(status=status.HTTP_200_OK)


class ChatroomViewSet(viewsets.ModelViewSet):
  """"""

  serializer_class = ChatroomSerializer
  queryset = Chatroom.objects.none()

  def get_queryset(self):
    queryset = Chatroom.objects.prefetch_related('messages').all().order_by(
        '-messages__sent_at')
    return queryset

  permission_classes = [MemberOrAdmin]

  @action(
      detail=True, methods=['post'], url_path=r'add-user/(?P<user_id>[^/.]+)')
  def add_user(self, request, pk: int, user_id: int):
    user: User = User.objects.get(id=user_id)
    chatroom: Chatroom = self.get_object()
    chatroom.users.add(user)
    return Response(status=status.HTTP_200_OK)

  @action(
      detail=True,
      methods=['delete'],
      url_path=r'remove-user/(?P<user_id>[^/.]+)')
  def remove_user(self, request, pk: int, user_id: int):
    user: User = User.objects.get(id=user_id)
    chatroom: Chatroom = self.get_object()
    chatroom.users.remove(user)
    return Response(status=status.HTTP_204_NO_CONTENT)
