from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group

from chat.models import Chatroom, Message, UserMessage


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


class MessageInline(admin.TabularInline):
  model = UserMessage
  extra = 1


class MessageForm(forms.ModelForm):

  class Meta:
    model = Message
    fields = (
        'text',
        'author',
        'chatroom',
    )
    widgets = {
        'author': forms.Select(),
        'chatroom': forms.Select(),
    }


class MessageAdmin(admin.ModelAdmin):
  list_display = ('text', 'author', 'sent_at')
  readonly_fields = ['sent_at', 'id']
  form = MessageForm
  inlines = (MessageInline,)


admin.site.register(Message, MessageAdmin)
