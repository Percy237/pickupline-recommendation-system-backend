from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, UserCategory, PickupLine, Rating


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "category_name"]


class UserCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCategory
        fields = ["user", "preferred_categories"]


class PickupLineSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="category.category_name", read_only=True
    )

    class Meta:
        model = PickupLine
        fields = ["id", "pickup_line", "category_name", "tags"]

        def get_category_name(self, obj):
            return obj.category.category_name


class RatingSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)

    class Meta:
        model = Rating
        fields = ["id", "user_id", "pickup_line", "rating"]


class PickupLineWithRatingSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    category_name = serializers.CharField(
        source="category.category_name", read_only=True
    )

    class Meta:
        model = PickupLine
        fields = ["id", "pickup_line", "category", "category_name", "tags", "rating"]

    def get_rating(self, obj):
        user = self.context["request"].user
        rating = Rating.objects.filter(user=user, pickup_line=obj)
        return rating.rating if rating else None

    def get_category_name(self, obj):
        return obj.category.category_name
