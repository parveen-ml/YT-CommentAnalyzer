import csv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import streamlit as st
from Senti import extract_video_id

import warnings
warnings.filterwarnings('ignore')

from dotenv import load_dotenv
import os
load_dotenv()

DEVELOPER_KEY = os.getenv('YOUTUBE_API_KEY')
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

def get_channel_id(video_id):
    try:
        response = youtube.videos().list(part='snippet', id=video_id).execute()
        if response['items']:
            return response['items'][0]['snippet']['channelId']
        else:
            st.warning("No video found with that ID.")
            return None
    except HttpError as e:
        st.error(f"Failed to fetch channel ID: {e}")
        return None

def save_video_comments_to_csv(video_id):
    comments = []
    try:
        results = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            maxResults=100
        ).execute()

        while results:
            for item in results['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                username = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
                comments.append([username, comment])

            if 'nextPageToken' in results:
                nextPage = results['nextPageToken']
                results = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    textFormat='plainText',
                    maxResults=100,
                    pageToken=nextPage
                ).execute()
            else:
                break

    except HttpError as e:
        st.error(f"Error fetching comments: {e}")
        return None

    if not comments:
        st.warning("No comments found for this video.")
        return None

    filename = f"{video_id}.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Username', 'Comment'])
        writer.writerows(comments)

    st.success(f"Fetched and saved {len(comments)} comments.")
    return filename

def get_video_stats(video_id):
    try:
        response = youtube.videos().list(part='statistics', id=video_id).execute()
        return response['items'][0]['statistics'] if response['items'] else {}
    except HttpError as e:
        st.error(f"Error fetching video statistics: {e}")
        return {}

def get_channel_info(youtube, channel_id):
    try:
        response = youtube.channels().list(
            part='snippet,statistics,brandingSettings',
            id=channel_id
        ).execute()

        if not response['items']:
            st.warning("No channel info found.")
            return None

        channel = response['items'][0]
        return {
            'channel_title': channel['snippet']['title'],
            'video_count': channel['statistics']['videoCount'],
            'channel_logo_url': channel['snippet']['thumbnails']['high']['url'],
            'channel_created_date': channel['snippet']['publishedAt'],
            'subscriber_count': channel['statistics']['subscriberCount'],
            'channel_description': channel['snippet']['description']
        }

    except HttpError as e:
        st.error(f"Error fetching channel info: {e}")
        return None
