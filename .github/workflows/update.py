# This script iterates a youtube channel and does the following:
# 1. Iterates over the playlists of the channel
# 2. Iterates over the videos of each playlist
# 3. Cretes a markdown file in the '_posts' directory for each playlist
# 4. Adds a markdown file for each  playlist, then creates a link to each video in the playlist

import os
import json
import requests

# Get the API key from the environment
api_key = os.environ.get('YOUTUBE_API_KEY')

# Get the channel id from the environment
channel_id = os.environ.get('YOUTUBE_CHANNEL_ID')

# using the youtube API iterate over the playlists
def get_playlists():
    url = f'https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId={channel_id}&key={api_key}'
    response = requests.get(url)
    return response.json()

# using the youtube API iterate over the videos in a playlist
def get_playlist_videos(playlist_id):
    url = f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={playlist_id}&key={api_key}'
    response = requests.get(url)
    return response.json()

# create a markdown file for each playlis which includes a link to each video
def create_markdown_file(playlist, videos):
    # get the playlist title
    title = playlist['snippet']['title']
    # get the playlist id
    playlist_id = playlist['id']

    publised_at = playlist['snippet']['publishedAt']
    # convert the date to a format that Jekyll understands
    date = publised_at.split('T')[0]

    # convert title to a format that can be used as a file name
    title_as_filename = title.replace(' ', '-').lower()

    # create a markdown file for the playlist
    with open(f'_posts/{date}-{title_as_filename}.md', 'w') as file:
        # write the front matter
        file.write('---\n')
        file.write(f'title: "{title}"\n')
        file.write('layout: post\n')
        file.write('---\n\n')
        # iterate over the videos in the playlist
        for video in videos['items']:
            # get the video title
            video_title = video['snippet']['title']
            # get the video id
            video_id = video['snippet']['resourceId']['videoId']

            # out te video title as a header
            file.write(f'## {video_title}\n')
            file.write(f'<iframe width="100%" height="600" src="https://www.youtube.com/embed/{video_id}" title="Polyhobbyist" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>\n\n')


# process youtube
playlists = get_playlists()
#iterate over the playlists
for playlist in playlists['items']:
    # get the playlist id
    playlist_id = playlist['id']
    # get the videos in the playlist
    videos = get_playlist_videos(playlist_id)
    # create a markdown file for the playlist
    create_markdown_file(playlist, videos)
