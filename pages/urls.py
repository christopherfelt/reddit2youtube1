from django.urls import path

from .views import SubredditListView, SubredditDetailView, GetSubredditPlaylist

urlpatterns = [
    path('', SubredditListView.as_view(), name='subreddit_list'),
    path('<int:pk>/', SubredditDetailView.as_view(), name='subreddit_detail'),
    path('getplaylist/<int:pk>/', GetSubredditPlaylist.as_view(), name='get_playlist'),
]
