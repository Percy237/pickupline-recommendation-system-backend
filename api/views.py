from random import shuffle
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from .serializers import (
    UserSerializer,
    CategorySerializer,
    PickupLineSerializer,
    RatingSerializer,
    UserProfileSerializer,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Category, PickupLine, Rating, UserProfile


class UserProfileListCreate(generics.ListCreateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, preferences_set=True)


class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class ListUsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PickupLineListCreate(generics.ListCreateAPIView):
    queryset = PickupLine.objects.all()
    serializer_class = PickupLineSerializer


class RatingListCreate(generics.ListCreateAPIView):
    serializer_class = PickupLineSerializer
    permission_classes = [IsAuthenticated]

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_queryset(self):
        user = self.request.user
        return Rating.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        pickup_line_id = serializer.validated_data["pickup_line"]
        rating_value = serializer.validated_data["rating"]
        existing_rating = Rating.objects.filter(
            user=user, pickup_line_id=pickup_line_id
        ).first()
        if existing_rating:
            existing_rating.rating = rating_value
            existing_rating.save()
            serializer = RatingSerializer(existing_rating)
        else:
            serializer = RatingSerializer(data=self.request.data)
            if serializer.is_valid():
                serializer.save(user=user)
            else:
                print("Serializer is not valid:", serializer.errors)


class PickupLineListWithRatings(APIView):
    def get(self, request):
        user = request.user
        user_profile = get_object_or_404(UserProfile, user=user)
        preferred_categories = user_profile.preferred_categories.all()

        pickup_lines = PickupLine.objects.filter(
            category__in=preferred_categories
        ).order_by("?")
        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of items per page
        pickup_lines = paginator.paginate_queryset(pickup_lines, request)

        serialized_pickup_lines = []
        for pickup_line in pickup_lines:
            ratings = Rating.objects.filter(user=user, pickup_line=pickup_line)
            serialized_ratings = [
                rating.rating for rating in ratings
            ]  # Extracting only rating values
            pickup_line_data = PickupLineSerializer(pickup_line).data
            pickup_line_data["ratings"] = serialized_ratings
            serialized_pickup_lines.append(pickup_line_data)

        return paginator.get_paginated_response(serialized_pickup_lines)
