from django.contrib.auth import get_user_model
from rest_framework import serializers

from chatappplus.chat.models import Chatroom, Message

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    exclude = ('chatrooms', 'sent_messages')


class MessageSerializer(serializers.ModelSerializer):
  author = serializers.PrimaryKeyRelatedField(read_only=True)
  chatroom = serializers.PrimaryKeyRelatedField(read_only=True)

  class Meta:
    model = Message
    fields = ('id', 'text', 'sent_at', 'read_at', 'author', 'chatroom')


class ChatroomSerializer(serializers.ModelSerializer):
  users = UserSerializer(many=True, read_only=True)
  last_message = serializers.SerializerMethodField()

  def get_last_message(self, obj):
    messages = obj.messages.all().order_by('-sent_at')
    if not messages.exists():
      return None
    message = messages[0]
    return MessageSerializer(message).data

  class Meta:
    model = Chatroom
    fields = ('id', 'name', 'users', 'last_message')
