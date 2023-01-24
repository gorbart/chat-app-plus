from django.contrib import admin
from chat.models import Chatroom, Message

admin.site.register(Chatroom)
admin.site.register(Message)
