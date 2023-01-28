from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import AdminSplitDateTime
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group

from chat.models import Chatroom, Message


class UserAdmin(UserAdmin):

  fieldsets = (
      (None, {
          'fields': ('username', 'password')
      }),
      (('Personal info'), {
          'fields': ('first_name', 'last_name', 'email')
      }),
      (('Permissions'), {
          'fields': ('is_active', 'is_staff', 'is_superuser'),
      }),
      (('Important dates'), {
          'fields': ('last_login', 'date_joined')
      }),
  )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.unregister(Group)

admin.site.register(Chatroom)


class MessageForm(forms.ModelForm):

  class Meta:
    model = Message
    fields = ('text', 'read_at', 'author', 'chatroom')
    widgets = {
        'read_at': AdminSplitDateTime(),
        'author': forms.Select(),
        'chatroom': forms.Select(),
    }


class MessageAdmin(admin.ModelAdmin):
  list_display = ('text', 'author', 'sent_at', 'read_at')
  readonly_fields = ['sent_at']
  form = MessageForm


admin.site.register(Message, MessageAdmin)
