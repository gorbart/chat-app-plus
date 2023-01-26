from django.contrib.auth.models import User
from django.core.exceptions import BadRequest
from rest_framework import viewsets

from chat.models import Message, Chatroom
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


class ChatroomViewSet(viewsets.ModelViewSet):
  """"""

  serializer_class = ChatroomSerializer
  queryset = Chatroom.objects.none()

  def get_queryset(self):
    queryset = Chatroom.objects.prefetch_related('messages').all().order_by(
        '-messages__sent_at')
    return queryset

  permission_classes = [MemberOrAdmin]
