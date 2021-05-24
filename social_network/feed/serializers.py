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
        if obj.creator.get_full_name() == "":
            return obj.creator.username

        return obj.creator.get_full_name()

    def get_likes(self, obj):
        return FeedLike.objects.filter(post=obj).count()

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
            "post",
            "created_at",
            "creator",
        ]

    def get_creator(self, obj):
        if obj.creator.get_full_name() == "":
            return obj.creator.username

        return obj.creator.get_full_name()

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)


class LikeSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()

    class Meta:
        model = FeedLike
        exclude = [
            "post",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "creator",
        ]

    def get_creator(self, obj):
        if obj.creator.get_full_name() == "":
            return obj.creator.username

        return obj.creator.get_full_name()

    def validate(self, data):
        is_liked = FeedLike.objects.filter(
            post=self.context["post"], creator=self.context["request"].user
        ).exists()
        if is_liked:
            raise serializers.ValidationError("You already liked this post")

        return data

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)
