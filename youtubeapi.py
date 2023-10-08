import os
import googleapiclient.discovery

# API KEY
API_KEY = 'AIzaSyB7D076dk1UGrD7_G7CSVlPDfS3j8HMsgE'

def get_video_comments(video_id, max_results=1):
    # Initialize the YouTube Data API client
    print("youtube api call 1")
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=API_KEY)
    print("youtube api call 2")
    # Fetch comments from the video
    try:
        comments = []
        nextPageToken = None
        print("youtube api call 3")
        while len(comments) < max_results:
            kwargs = {
                'part': 'snippet',
                'videoId': video_id,
                'textFormat': 'plainText',
                'maxResults': max_results - len(comments),
                'pageToken': nextPageToken
            }
            print("youtube api call 4")
            results = youtube.commentThreads().list(**kwargs).execute()
            print("youtube api call 5")
            for item in results.get('items', []):
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)
            print("youtube api call 6")
            nextPageToken = results.get('nextPageToken')
            print("youtube api call 7")
            if not nextPageToken:
                break

    except Exception as e:
        # Handle any exceptions that occur during the API request
        print(f"Error fetching comments: {str(e)}")

    return comments