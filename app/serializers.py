from rest_framework import serializers

from .models import User, Post, UserFollowing, Feed


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('user', 'body')

class UserFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = ('user', 'user_to_follow')

class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ('id', 'body', 'author', 'likes')
