from django.urls import path
from .views import PostListView, PostDetailView
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path("post-list/", views.PostListView.as_view(), name="post-list"),
    path("post/<slug:slug>/", views.PostDetailView.as_view(),
         name="post-detail"),
]
