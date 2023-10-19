from django.urls import path
from .views import PostListView, PostDetailView, create_post, PostEditView
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path("post-list/", views.PostListView.as_view(), name="post-list"),
    path("post/<slug:slug>/", views.PostDetailView.as_view(),
         name="post-detail"),
    path('create-post/', views.create_post, name='create-post'),
    path('post/edit/<slug:slug>/', PostEditView.as_view(), name='post-edit'),
]
