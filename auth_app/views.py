from django.contrib.auth import authenticate, get_user_model, login
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import CreateView
from rest_framework import status, authentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from auth_app.forms import LoginForm
from auth_app.models import UserOTP
from auth_app.serializers import LoginSerializer, UserSerializer, OTPSerializer

User = get_user_model()


class SendOTPView(CreateAPIView):
    serializer_class = OTPSerializer


class UserLogin(CreateAPIView):
    serializer_class = LoginSerializer
    queryset = User.objects.none()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['phone_number']
        otp = serializer.validated_data['otp']
        token, created = Token.objects.get_or_create(user=user)
        last_login = user.last_login
        user.last_login = timezone.now()
        user.save()
        if last_login is None:
            return Response({
                'token': token.key,
                'first_time': True
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'token': token.key
            }, status=status.HTTP_200_OK)
        # groups = user.user_permissions.all()
        # groups = user.get_all_permissions()


class UserRegistration(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return Response(data=self.serializer_class(User.objects.all(), many=True).data)
        else:
            return Response(data={"message": "You do not have permissions"})


class LogoutUser(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request, format=None):
        Token.objects.get(user=request.user).delete()
        return Response(status=status.HTTP_200_OK)


class AdminLoginPageView(View):
    template_name = 'admin.login.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, {'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['phone_number'],
                password=form.cleaned_data['password'],
            )
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect(reverse_lazy('main:dashboard'))
        message = 'Login failed!'
        return render(request, self.template_name, context={'form': form, 'message': message})


@ensure_csrf_cookie
@api_view(['GET'])
def login_set_cookie(request):
    if request.method == 'GET':
        return Response(status=status.HTTP_200_OK)
