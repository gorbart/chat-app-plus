from django.contrib.auth.models import User
from rest_framework import mixins, viewsets

from chat.models import Message, Chatroom
from chat.serializers import (MessageSerializer, ChatroomSerializer,
                              UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows users to be viewed or edited.
  """
  queryset = User.objects.all().order_by('-date_joined')
  serializer_class = UserSerializer


class ChatMessageViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
  """
  API endpoint that allows chat messages to be viewed or edited.
  """
  queryset = Message.objects.all().order_by('-sent_at')
  serializer_class = MessageSerializer


class ChatroomViewSet(viewsets.ModelViewSet):
  """"""

  serializer_class = ChatroomSerializer
  queryset = Chatroom.objects.none()

  def get_queryset(self):
    queryset = Chatroom.objects.prefetch_related('messages').all().order_by(
        '-messages__sent_at')
    return queryset
