from asgiref.sync import sync_to_async
from urllib.parse import parse_qs
from jwt import decode as decode_jwt

from channels.auth import AuthMiddlewareStack
from channels.middleware import BaseMiddleware
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken

User = get_user_model()


class JWTAuthMiddleware(BaseMiddleware):

  def __init__(self, inner):
    self.inner = inner

  async def __call__(self, scope, receive, send):

    close_old_connections()

    token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]

    try:
      UntypedToken(token)
    except (InvalidToken, TokenError):
      return AnonymousUser()

    decoded_data = decode_jwt(token, settings.SECRET_KEY, algorithms=["HS256"])

    scope["user"] = await sync_to_async(User.objects.get)(
        id=decoded_data["user_id"])

    return await super().__call__(scope, receive, send)


def JWTAuthMiddlewareStack(inner):
  return JWTAuthMiddleware(AuthMiddlewareStack(inner))
