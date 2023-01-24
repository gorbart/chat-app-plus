from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Chatroom(models.Model):
  name = models.CharField(max_length=255)
  users = models.ManyToManyField(User, related_name='chatrooms')

  def __str__(self) -> str:
    return self.name


class Message(models.Model):
  text = models.TextField()
  sent_at = models.DateTimeField(auto_now_add=True)
  read_at = models.DateTimeField(null=True, blank=True)
  author = models.ForeignKey(
      User, on_delete=models.CASCADE, related_name='sent_messages')
  chatroom = models.ForeignKey(
      Chatroom, on_delete=models.CASCADE, related_name='messages')

  def __str__(self) -> str:
    return self.author.get_username() + ': ' + self.text
