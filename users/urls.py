from django.urls import include, path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from .views import ContactView, CustomLogoutView
from .views import (
    MyTokenObtainPairView,
    UserCreateAPIView,
    UserViewSet,
    HomeView,
    RegisterView,
    UserLoginView,
    HomeLoginView,
)

app_name = "users"

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("api/", include(router.urls)),
    path(
        "api/login/",
        MyTokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="api_login",
    ),
    path("api/register/", UserCreateAPIView.as_view(), name="api_register"),
    path("register/", RegisterView.as_view(), name="register"),
    path("home_login/", HomeLoginView.as_view(), name="home_login"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
]
