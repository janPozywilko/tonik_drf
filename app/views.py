import re
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import JsonResponse, HttpResponse


from dispo.settings import DATABASES

import json

from .models import Post, PostLike, Feed

from .serializers import UserFollowingSerializer, UserSerializer, PostSerializer, UserFollowing


@api_view(["POST"])
def create_user(request):

    serializer_data = UserSerializer(data=request.data, many=False)
    if(serializer_data.is_valid()):
        serializer_data.save()
        return Response({"message": "user was created sucesfully"}, status=status.HTTP_201_CREATED)
    
    return Response({"error": "there was an error creating user"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_post(request):

    try:
        user = User.objects.get(id=request.user.id)
    except:
        return Response({"message": "sorry user not found"}, status=status.HTTP_400_BAD_REQUEST)
    
    data = {}
    data["user"] = user.id
    body = request.data['body']    
    data["body"] = body 

    serializer_class = PostSerializer(data=data, many=False)

    if(serializer_class.is_valid()):
        serializer_class.save()
        return Response({"message": f"post was created for user {user}"}, status=status.HTTP_201_CREATED)

    print(serializer_class.errors)


    return Response({"message": "post was not created"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def users_top(request):
    
    user_top = []
    users = User.objects.all()

    for user in users:
        user_info = {}
        post_count = user.posts.all().count()
        user_info["username"] = user.username
        user_info["posts"] = post_count
        user_top.append(user_info)

    return Response(user_top, status=status.HTTP_200_OK)

@api_view(["POST"])
def users_follow(request):
    
    serializer_data = UserFollowingSerializer(data=request.data, many=False)

    if(serializer_data.is_valid()):
        serializer_data.save()
        return Response({"message": "user was followed sucessfully"}, status=status.HTTP_200_OK)

    print(serializer_data.error_messages)

    return Response({"error_message": "user was not followed sucessfully"}, status=status.HTTP_400_BAD_REQUEST)

def get_likes_for_post(post_id):

    post_like_count = PostLike.objects.filter(post=post_id).count()

    return post_like_count

@api_view(["GET"])
def user_feed(request, user_id):

    posts = []

    posts_for_user = Post.objects.filter(user_id=int(user_id))

    [posts.append(Feed(id=post.id, body=post.body, timestamp=post.timestamp ,author=post.user.username, likes=get_likes_for_post(post.id))) for post in posts_for_user]

    following_accounts = UserFollowing.objects.filter(user_id=int(user_id))

    for account in following_accounts:
        posts_for_following_user = Post.objects.filter(user_id=int(account.user_to_follow.id))
        [posts.append(Feed(id=following_post.id, body=following_post.body, timestamp=following_post.timestamp, author=following_post.user.username, likes=get_likes_for_post(following_post.id))) for following_post in posts_for_following_user]

    posts.sort(key=lambda x: x.timestamp, reverse=True)

    response = json.dumps([post.to_dict() for post in posts])

    return HttpResponse(response, content_type="application/json")