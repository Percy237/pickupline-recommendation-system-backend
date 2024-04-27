from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, PickupLine, Rating, UserProfile


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CategorySerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source="id")

    class Meta:
        model = Category
        fields = ["category_id", "category_name"]


class UserProfileSerializer(serializers.ModelSerializer):
    preferred_categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all(),
        required=True,
        allow_empty=False,
    )

    class Meta:
        model = UserProfile
        fields = ["id", "preferred_categories", "preferences_set"]

    def validate_preferred_categories(self, value):
        if not value:
            raise serializers.ValidationError("You must select at least one category.")
        return value


class PickupLineSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="category.category_name", read_only=True
    )

    pickup_line_id = serializers.IntegerField(source="id")

    class Meta:
        model = PickupLine
        fields = ["pickup_line_id", "pickup_line", "category_name", "tags"]

        def get_category_name(self, obj):
            return obj.category.category_name


class RatingSerializer(serializers.ModelSerializer):

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
