from django.urls import path
from . import views

urlpatterns = [
    path("profile/", views.UserCategoryListCreate.as_view(), name="user-profile"),
    path(
        "categories/", views.CategoryListCreate.as_view(), name="category-list-create"
    ),
    path(
        "categories/<int:pk>/",
        views.CategoryRetrieveUpdateDestroy.as_view(),
        name="category-destroy",
    ),
    path(
        "pickup-lines/",
        views.PickupLineListCreate.as_view(),
        name="pickup-line-list-create",
    ),
    path("ratings/", views.RatingListCreate.as_view(), name="rating-list-create"),
    path(
        "pickup-lines/<int:pk>/rate/",
        views.RatingUpdate.as_view(),
        name="pickup-line-rate",
    ),
]

#    path(
#         "pickup-lines-ratings/",
#         views.PickupLineWithRatingsListView.as_view(),
#         name="pickup-line-with-ratings-list-create",
#     ),
