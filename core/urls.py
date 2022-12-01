from django.urls import path
from .views import (
    RegisterUser, Index, UserAuth, UserLogout,
    Test, Stats
)


urlpatterns = [
    path("", Index.as_view(), name="index_page"),
    path("reg", RegisterUser.as_view(), name="reg_page"),
    path("auth", UserAuth.as_view(), name="auth_page"),
    path("logout", UserLogout.as_view(), name="logout_page"),
    path("test/<int:test_id>", Test.as_view()),
    path("stats", Stats.as_view(), name="stats_page"),
]
