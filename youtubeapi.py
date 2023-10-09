import os
import googleapiclient.discovery

# Initialize the YouTube Data API client with an API key
def initialize_youtube_client(api_key):
    return googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

def get_video_comments(video_id, max_results=1, api_key=None):
    # Initialize the YouTube Data API client
    if api_key is None:
        raise ValueError("API key is required")
    youtube = initialize_youtube_client(api_key)

    # Fetch comments from the video
    try:
        comments = []
        nextPageToken = None
        while len(comments) < max_results:
            kwargs = {
                'part': 'snippet',
                'videoId': video_id,
                'textFormat': 'plainText',
                'maxResults': max_results - len(comments),
                'pageToken': nextPageToken
            }
            results = youtube.commentThreads().list(**kwargs).execute()
            for item in results.get('items', []):
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)
            nextPageToken = results.get('nextPageToken')
            if not nextPageToken:
                break

    except Exception as e:
        # Handle any exceptions that occur during the API request
        print(f"Error fetching comments: {str(e)}")

    return comments