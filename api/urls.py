from django.urls import path
from . import views

urlpatterns = [
    path("users/all/", views.ListUsersView.as_view(), name="list-users"),
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
    path(
        "pickup-lines-ratings/",
        views.PickupLineListWithRatings.as_view(),
        name="pickup-line-list-create",
    ),
    path("ratings/", views.RatingListCreate.as_view(), name="rating-list-create"),
    path("userprofile/", views.UserProfileListCreate.as_view(), name="userprofile"),
]

#    path(
#         "pickup-lines-ratings/",
#         views.PickupLineWithRatingsListView.as_view(),
#         name="pickup-line-with-ratings-list-create",
#     ),
