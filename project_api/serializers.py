from rest_framework import serializers

from accounts.models import Profile
from services.models import News, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name",)


class NewsSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    is_published = serializers.BooleanField(read_only=True, default=True)
    image = serializers.ImageField(required=False)
    slug = serializers.CharField(read_only=True)

    class Meta:
        model = News
        fields = "__all__"

    def to_representation(self, instance):
        """Adds data from the associated table about the tag to the resulting data."""
        rep_data = super().to_representation(instance)
        rep_data["tag"] = TagSerializer(instance.tag).data
        return rep_data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("nickname", "bio", "location", "birth_date", "photo", "id")
