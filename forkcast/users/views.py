from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token

from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import SignInSerializer, UserSerializer

@csrf_protect
@api_view(["POST"])
@permission_classes([AllowAny])
def sign_in(request):

    serializer = SignInSerializer(data=request.data)
    if not serializer.is_valid(raise_exception=True):
        return Response(
            {
                "message": "Please check your input",
                "errors": serializer.errors,
            },
            status = status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(
        request=request,
        email=serializer.validated_data["email"],
        password=serializer.validated_data["password"],
    )

    if user is None:
        return Response(
            {"message": "Invalid email or password."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    login(request, user)

    return Response(
        {
            "message": "Signed in successfully.",
            "user": UserSerializer(user).data,
        },
        status=status.HTTP_200_OK,
    )

@csrf_protect
@api_view(["POST"])
@permission_classes([AllowAny])
def sign_out(request):
    logout(request)
    return Response(status=status.HTTP_204_NO_CONTENT) 

@api_view(["GET"])
@permission_classes([AllowAny])
def current_user(request):
    if not request.user.is_authenticated:
        return Response(
            {"message": "You are not signed in."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    return Response(UserSerializer(request.user).data)

@api_view(["GET"])
@permission_classes([AllowAny])
def csrf_token(request):
    return Response({
        "csrfToken": get_token(request),
    })

