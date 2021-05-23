from rest_framework import serializers
from .models import FeedPost, FeedComment, FeedLike


class PostSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    like = serializers.SerializerMethodField()

    class Meta:
        model = FeedPost
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "creator",
        ]

    def get_creator(self, obj):
        return obj.creator.get_full_name()

    def get_like(self, obj):
        return FeedLike.objects.filter(feed=obj).count()

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()

    class Meta:
        model = FeedComment
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "creator",
        ]

    def get_creator(self, obj):
        return obj.creator.get_full_name()

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)


class LikeSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()

    class Meta:
        model = FeedLike
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "creator",
        ]

    def get_creator(self, obj):
        return obj.creator.get_full_name()

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user

        liked = FeedLike.objects.filter(
            feed=validated_data["feed"], creator=validated_data["creator"]
        )
        if not liked.exists():
            return super().create(validated_data)

        return liked.first()