from django.urls import re_path
from rest_framework import routers

from chat.consumers import ChatConsumer
from chat.views import ChatroomViewSet, MessageViewSet, UserViewSet

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'chatrooms', ChatroomViewSet)
router.register(r'messages', MessageViewSet, basename='Message')
urlpatterns = router.urls

websocket_urlpatterns = [
    re_path(r"ws/chatroom/(?P<chatroom_id>\w+)/$", ChatConsumer.as_asgi())
]
