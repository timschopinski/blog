from django.urls import path
from . import views
urlpatterns = [
    path("", views.StartingPageView.as_view(), name="starting_page"),
    path("posts", views.AllPostsView.as_view(), name="posts-page"),
    path("posts/<slug:slug>", views.SinglePostView.as_view(), name="post-detail-page"),
    path("read-later", views.ReadLaterView.as_view(), name="read-later"),
    path("remove", views.RemoveFromReadLaterView.as_view(), name="remove"),
    path("add-post", views.AddPostView.as_view(), name="add-post")
]