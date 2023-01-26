from rest_framework import permissions

from chat.models import Chatroom


class SelfOrAdmin(permissions.BasePermission):

  def has_permission(self, request, view):
    return request.user.is_authenticated

  def has_object_permission(self, request, view, obj):

    if request.method in permissions.SAFE_METHODS:
      return True

    return request.user.is_staff == True or request.user == obj


class MemberOrAdmin(permissions.BasePermission):

  def has_permission(self, request, view):
    return request.user.is_authenticated

  def has_object_permission(self, request, view, obj):

    return request.user.is_staff == True or request.user in obj.users.all()


class ChatroomMemberOrAdmin(permissions.BasePermission):

  def has_permission(self, request, view):
    chatroom_id = request.query_params.get('chatroom_id')

    chatroom = Chatroom.objects.get(id=chatroom_id)
    if request.user.is_staff == True or request.user in chatroom.users.all():
      return True

    return False

  def has_object_permission(self, request, view, obj):
    return request.user.is_staff == True or request.user in obj.chatroom.users.all(
    )
