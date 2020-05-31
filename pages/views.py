from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, View

from allauth.socialaccount.models import SocialToken



from google.oauth2.credentials import Credentials

from .models import Subreddit
from .r2u import get_youtube_ids, get_playlist

# class SubredditListView(TemplateView):
#     template_name = 'subreddit_list.html'


class SubredditListView(ListView):
    template_name = 'subreddit_list.html'
    model = Subreddit
    context_object_name = 'subreddits'


class SubredditDetailView(DetailView):
    template_name = 'subreddit_detail.html'

    model = Subreddit
    context_object_name = 'subreddits'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # subreddit_name = Subreddit.objects.filter(
        #     pk=self.kwargs['pk']
        # ).values('name')[0]['name']
        subreddit_name = Subreddit.objects.get(pk=self.kwargs['pk'])
        video_ids = get_youtube_ids(subreddit_name.name)
        context["video_ids"] = video_ids
        return context


class GetSubredditPlaylist(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        # token = SocialToken.objects.filter(account__user=user,
        #                                    account__provider='google').values('token')[0]['token']
        social_token = SocialToken.objects.get(account__user=user)
        creds = Credentials(token=social_token.token,
                            refresh_token=social_token.token_secret,
                            token_uri='https://127.0.0.1/',
                            client_id='969760717898-cavisob2kugm592qqvfs9a8easplo0rh.apps.googleusercontent.com',
                            client_secret='fuNrq_oVxniyGNch8u5_x_fQ')

        subreddit_name = Subreddit.objects.get(pk=self.kwargs['pk'])
        video_ids = get_youtube_ids(subreddit_name.name)
        get_playlist(creds, video_ids)

        return render(request, 'successful_download.html')
        
