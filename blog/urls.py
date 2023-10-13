from django.urls import path
from .views import PostListView, PostDetailView
from . import views


urlpatterns = [
    path("", views.PostListView.as_view(), name="home"),
    path("post/<slug:slug>/", views.PostDetailView.as_view(),
         name="post-detail"),
]
