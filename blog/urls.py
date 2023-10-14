from django.urls import path
from .views import PostListView, PostDetailView
from . import views


urlpatterns = [
    # path("", views.PostListView.as_view(), name="home"),
    path('', views.index, name='home'),
    path("post-list/", views.PostListView.as_view(), name="post-list"),
    path("post/<slug:slug>/", views.PostDetailView.as_view(),
         name="post-detail"),
]

# urlpatterns = [
#     path("", views.PostListView.as_view(), name="home"),
#     path("post/<slug:slug>/", views.PostDetailView.as_view(),
#          name="post-detail"),
# ]
