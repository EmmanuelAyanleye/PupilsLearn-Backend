from django.urls import path
from .views import (
    StudentRegisterView,
    SelfDetailView,
    AdminUpdateUserView,
    LogoutView,
)

urlpatterns = [
    path("register/student/", StudentRegisterView.as_view(), name="student-register"),
    path("me/", SelfDetailView.as_view(), name="me"),
    path("admin/users/<int:pk>/", AdminUpdateUserView.as_view(), name="admin-update-user"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
