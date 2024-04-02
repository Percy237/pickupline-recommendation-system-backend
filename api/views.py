from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import (
    UserSerializer,
    UserCategorySerializer,
    CategorySerializer,
    PickupLineSerializer,
    RatingSerializer,
    PickupLineWithRatingSerializer,
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
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            print(serializer.errors)


class RatingUpdate(generics.UpdateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Rating.objects.filter(user=user)
    
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    # def perform_update(self, serializer):
    #     user = self.request.user
    #     pickup_line_id = self.kwargs.get("pk")
    #     rating_value = self.request.data.get("rating")

    #     # Get or create the rating object
    #     rating, created = Rating.objects.get_or_create(
    #         user=user, pickup_line_id=pickup_line_id
    #     )

    #     # Update the rating value
    #     rating.rating = rating_value
    #     rating.save()


# class PickupLineWithRatingsListView(generics.ListAPIView):
#     queryset = PickupLine.objects.all()
#     serializer_class = PickupLineWithRatingSerializer
#     permission_classes = [IsAuthenticated]
