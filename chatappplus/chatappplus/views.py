from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import ExtendedTokenObtainPairSerializer


class ExtendedTokenObtainPairView(TokenObtainPairView):
  serializer_class = ExtendedTokenObtainPairSerializer
