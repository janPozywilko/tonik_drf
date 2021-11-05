from django.urls import path
from .views import create_post, create_user, users_top, users_follow, user_feed

urlpatterns = [
    path('user/create/', create_user),
    path('post/create/', create_post),
    path('users/top', users_top),
    path('users/follow', users_follow),
    path('users/feed/<int:user_id>/', user_feed)
]
