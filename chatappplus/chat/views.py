from django.contrib.auth.models import User
from rest_framework import mixins, viewsets

from chat.models import Message, Chatroom
from chat.serializers import (MessageSerializer, ChatroomSerializer,
                              UserSerializer)
from chat.permissions import (ChatroomMemberOrAdmin, MemberOrAdmin, SelfOrAdmin)


class UserViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows users to be viewed or edited.
  """
  queryset = User.objects.all().order_by('-date_joined')
  serializer_class = UserSerializer

  permission_classes = [SelfOrAdmin]


class MessageViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
  """
  API endpoint that allows chat messages to be viewed or edited.
  """
  queryset = Message.objects.all().order_by('-sent_at')
  serializer_class = MessageSerializer

  permission_classes = [ChatroomMemberOrAdmin]


class ChatroomViewSet(viewsets.ModelViewSet):
  """"""

  serializer_class = ChatroomSerializer
  queryset = Chatroom.objects.none()

  def get_queryset(self):
    queryset = Chatroom.objects.prefetch_related('messages').all().order_by(
        '-messages__sent_at')
    return queryset

  permission_classes = [MemberOrAdmin]
