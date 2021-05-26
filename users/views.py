from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import CustomUser
from .serializers import CustomUserSerializer


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    # permission_classes = [IsAdminUser]

    @action(detail=False, methods=["get"], url_path="is_email_busy/(?P<email>.+)")
    def is_email_busy(self, request, email=None):
        if CustomUser.objects.filter(email=email):
            return Response({"message": "Email is already in use."})
        else:
            return Response({"message": "Email is available."})

    @action(detail=False, methods=["get"], url_path="is_username_busy/(?P<username>.+)")
    def is_username_busy(self, request, username=None):
        if CustomUser.objects.filter(username=username):
            return Response({"message": "Username is already in use."})
        else:
            return Response({"message": "Username is available."})


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(
                data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        except ValidationError:
            raise AuthenticationFailed()
