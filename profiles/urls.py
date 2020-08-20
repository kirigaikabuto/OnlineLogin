from django.urls import path
from . views import *

urlpatterns = [
    path('register/', register_page, name='register_page'),
    path("login/", login_page, name="login_page"),
    path("profile/", profile_page, name="profile_page"),
    path("logout/", log_out, name="log_out"),
    path("order_friend_action/<int:profile_pk>/", order_friend_action, name="order_friend_action"),
]

