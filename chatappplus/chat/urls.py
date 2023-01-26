from rest_framework import routers

from chat.views import ChatroomViewSet, MessageViewSet, UserViewSet

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'chatrooms', ChatroomViewSet)
router.register(r'messages', MessageViewSet, basename='Message')
urlpatterns = router.urls
