from asgiref.sync import sync_to_async
from datetime import datetime, timezone
import json
from typing import List

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import DenyConnection

from chat.models import Chatroom, Message, UserMessage
from chat.serializers import MessageSerializer


class ChatConsumer(AsyncWebsocketConsumer):

  async def connect(self):
    self.chatroom: Chatroom = await sync_to_async(Chatroom.objects.get)(
        id=self.scope["url_route"]["kwargs"]["chatroom_id"])

    self.user = self.scope["user"]

    self.room_name = self.chatroom.name + "_" + str(self.chatroom.id)
    self.room_group_name = "chat_" + self.room_name

    if await sync_to_async(self.check_if_user_in_chatroom)(self.chatroom
                                                          ) == False:
      raise DenyConnection("User is not in chatroom")

    await self.channel_layer.group_add(self.room_group_name, self.channel_name)

    await self.accept()

    messages = await sync_to_async(self.get_last_50_messages)(self.chatroom)
    await self.send(
        json.dumps({
            "type":
                "last_50_messages",
            "messages": (await sync_to_async(self.serialize_messages)
                         (messages)),
        }))

  def get_last_50_messages(self, chatroom: Chatroom) -> List[Message]:
    messages = chatroom.messages.all().order_by('-sent_at')[:50]
    return messages

  def serialize_messages(self, messages: List[Message]) -> List[dict]:
    return MessageSerializer(messages, many=True).data

  def check_if_user_in_chatroom(self, chatroom: Chatroom) -> bool:
    users = chatroom.users.all()
    return self.user in users

  async def disconnect(self, close_code: int):

    await self.channel_layer.group_discard(self.room_group_name,
                                           self.channel_name)

  async def receive(self, text_data: str):
    text_data_json: dict = json.loads(text_data)
    message: str = text_data_json["message"]

    await self.channel_layer.group_send(self.room_group_name, {
        "type": "chat_message",
        "message": message
    })

  async def chat_message(self, event: dict):
    message_text: str = event["message"]

    chatroom_id: int = self.chatroom.id

    message: Message = await sync_to_async(Message.objects.create
                                          )(text=message_text,
                                            sent_at=datetime.now(timezone.utc),
                                            author=self.scope["user"],
                                            chatroom=await
                                            sync_to_async(Chatroom.objects.get)
                                            (id=chatroom_id))

    await self.send(
        text_data=json.dumps({
            "message": message.text,
            "author": message.author.username,
            "sent_at": message.sent_at
        }))
