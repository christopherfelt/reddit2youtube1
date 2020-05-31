import os
import praw
import re
from datetime import datetime

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# from allauth.socialaccount.models import SocialToken

#  Reddit TODO -- Move Credentials to Environment
reddit_cid = os.environ('REDDIT_CLIENT_ID')
reddit_sec = os.environ('REDDIT_CLIENT_SECRET')

reddit = praw.Reddit(client_id=reddit_cid,
                     client_secret=reddit_sec,
                     user_agent='me')


def get_youtube_ids(music_subreddit,
                    return_posts_number=20,
                    hot=False,
                    return_data=False,
                    print_other_url=False
                    ):

    song_id_list = []

    yt_count = 0
    spot_count = 0
    sc_count = 0
    other_urls = []

    music_subreddit = reddit.subreddit(music_subreddit)
    post_list = music_subreddit.hot(limit=return_posts_number)

    for post in post_list:
        post_url = post.url
        split_url = post_url.split('/')
        post_created = datetime.fromtimestamp(post.created_utc)
        re_pattern = r'=(.*)'
        if split_url[2] == 'youtu.be':
            song_id = split_url[3]
            if len(song_id) > 11:
                re_pattern = r'(.*)\?'
                song_id = re.search(re_pattern, song_id)
                song_id = song_id.group(1)
            song_id_list.append(song_id)
            yt_count += 1
        elif split_url[2] == 'www.youtube.com':
            song_id = re.search(re_pattern, split_url[3])
            yt_count += 1
            try:
                song_id = song_id.group(1)
                if len(song_id) > 11:
                    re_pattern = r'(.*)\&'
                    song_id = re.search(re_pattern, song_id)
                    song_id = song_id.group(1)
            except e:
                song_id = split_url[3]
            song_id_list.append(song_id)
        else:
            song_id = 'Not Youtube'
            if "spotify" in split_url[2]:
                spot_count += 1
            elif "soundcloud" in split_url[2]:
                sc_count += 1
            else:
                other_urls.append(split_url[2])

        current_time = datetime.now()

        post_age = current_time - post_created

        if return_data:
            print("Post Title: " + post.title + ", "
                  + "Post Url: " + post.url + ", "
                  + "Song ID: " + song_id + ", "
                  + "Post Date: " + str(post_created) + ", "
                  + "Post Age: " + str(post_age))

    if return_data:
        print("")
        print("Total Youtube Count: " + str(yt_count))
        print("Total Spotify Count: " + str(spot_count))
        print("Total SoundCloud Count: " + str(sc_count))
        print("Total Other Url: " + str(len(other_urls)))
        print("")

    return song_id_list


def get_playlist(credentials, video_ids):

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
                                              api_service_name, api_version,
                                              credentials=credentials)

    request = youtube.playlists().insert(
        part="snippet,status",
        body={
          "snippet": {
            "title": "TestPlaylist-3",
            "description": "Testing Playlist",
            "tags": [
              "sample playlist",
              "API call"
            ],
            "defaultLanguage": "en"
          },
          "status": {
            "privacyStatus": "private"
          }
        }
    )
    response = request.execute()

    playlistID = response['id']

    # print(response)

    for v_id in video_ids:
        request = youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlistID,
                    "position": 0,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": v_id
                    }
                }
            }
        )
        response = request.execute()
