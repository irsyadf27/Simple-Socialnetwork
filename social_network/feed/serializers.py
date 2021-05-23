from rest_framework import serializers


from feed.models import FeedComment, FeedLike, FeedPost


class PostSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

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

    def get_likes(self, obj):
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

    def validate(self, data):
        is_liked = FeedLike.objects.filter(
            feed=data.get("feed"), creator=data.get("creator")
        ).exists()
        if is_liked:
            raise serializers.ValidationError("You already liked this feed")

        return data

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)
