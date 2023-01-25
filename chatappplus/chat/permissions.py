from rest_framework import permissions


class SelfOrAdmin(permissions.BasePermission):

  def has_object_permission(self, request, view, obj):

    if request.method in permissions.SAFE_METHODS:
      return True

    return request.user.is_staff == True or request.user == obj


class MemberOrAdmin(permissions.BasePermission):

  def has_object_permission(self, request, view, obj):

    return request.user.is_staff == True or request.user in obj.users.all()


class ChatroomMemberOrAdmin(permissions.BasePermission):

  def has_object_permission(self, request, view, obj):

    return request.user.is_staff == True or request.user in obj.chatroom.users.all(
    )
