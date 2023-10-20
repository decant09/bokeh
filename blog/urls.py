from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    create_post,
    PostEditView,
    PostDeleteView,
    CommentDeleteView
)
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path("post-list/", views.PostListView.as_view(), name="post-list"),
    path("post/<slug:slug>/", views.PostDetailView.as_view(),
         name="post-detail"),
    path('create-post/', views.create_post, name='create-post'),
    path('post/edit/<slug:slug>/', PostEditView.as_view(), name='post-edit'),
    path('post/delete/<slug:slug>/', PostDeleteView.as_view(),
         name='post-delete'),
    path('post/<slug:slug>/comment/delete/<int:pk>/',
         CommentDeleteView.as_view(), name='comment-delete'),
]
