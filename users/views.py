from django.contrib.auth import get_user_model, login
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers import MyTokenObtainPairSerializer, UserSerializer
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from users.forms import CustomUserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


User = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class HomeView(TemplateView):
    template_name = "users/home.html"


class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:home_login")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Автоматический логин после регистрации
        print(f"User {user.email} successfully registered!")
        return super().form_valid(form)


class HomeLoginView(TemplateView):
    template_name = "users/home_login.html"


class UserLoginView(LoginView):
    template_name = "users/login.html"  # Указываем шаблон логина
    redirect_authenticated_user = True  # Если юзер уже вошел, отправить его на главную
    next_page = reverse_lazy("users:home_login")  # Куда перенаправить после входа

    def get(self, request, *args, **kwargs):
        """Обрабатываем GET-запрос (открытие страницы логина)"""
        if request.user.is_authenticated:
            return redirect(
                self.next_page
            )  # Если юзер уже залогинен, перенаправляем его
        return super().get(
            request, *args, **kwargs
        )  # Если не залогинен, показываем страницу

    def post(self, request, *args, **kwargs):
        """Обрабатываем POST-запрос (отправка формы логина)"""
        response = super().post(request, *args, **kwargs)
        if request.user.is_authenticated:  # Проверяем, успешно ли вошел пользователь
            request.session.set_expiry(0)  # Сессия сбрасывается при выходе
        return response


class ContactView(TemplateView):
    template_name = "users/contact.html"  # Контакты


@method_decorator(csrf_exempt, name="dispatch")  # Убираем CSRF ошибки
class CustomLogoutView(LogoutView):
    """После выхода удаляет сессию и перенаправляет на главную страницу."""

    def post(self, request, *args, **kwargs):
        request.session.flush()  # Очищает сессию полностью
        return redirect("users:home")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
