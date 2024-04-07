from random import shuffle
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from .serializers import (
    UserSerializer,
    UserCategorySerializer,
    CategorySerializer,
    PickupLineSerializer,
    RatingSerializer,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import UserCategory, Category, PickupLine, Rating


class UserCategoryListCreate(generics.ListCreateAPIView):
    serializer_class = UserCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return UserCategory.objects.filter(user=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            print(serializer.errors)


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
        return Rating.objects.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user
        pickup_line_id = serializer.validated_data["pickup_line"]
        rating_value = serializer.validated_data["rating"]
        print(rating_value)
        existing_rating = Rating.objects.filter(
            user=user, pickup_line_id=pickup_line_id
        ).first()
        print(existing_rating)
        if existing_rating:
            existing_rating.rating = rating_value
            existing_rating.save()
            serializer = RatingSerializer(existing_rating)
            # User has already rated this pickup line, return a 403 response
        else:
            serializer = RatingSerializer(data=self.request.data)
            if serializer.is_valid():  # Check if the serializer is valid
                serializer.save(user=user)
            else:
                # Handle the case where serializer is not valid
                # You can return an error response or perform other actions
                print("Serializer is not valid:", serializer.errors)


class PickupLineListWithRatings(APIView):
    pagination_class = PageNumberPagination

    def get(self, request):
        user = request.user
        pickup_lines = PickupLine.objects.all()

        paginator = self.pagination_class()
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
            shuffle(serialized_pickup_lines)

        return paginator.get_paginated_response(
            serialized_pickup_lines,
        )
