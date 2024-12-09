import yt_dlp
from youtubesearchpython import VideosSearch
import os
import conversion  # Make sure this is properly imported


# Download video and convert to data (generic function)
def download_video(video_id):
    try:
        # Download the video (no audio) using yt-dlp
        ydl_opts = {
            'format': 'bestvideo',
            'outtmpl': f'./user_data/{video_id}.mp4',
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferredcodec': 'mp4',
                'preferredquality': 'best',
            }],
            'postprocessor_args': ['-an'],  # '-an' disables audio
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f'https://www.youtube.com/watch?v={video_id}'])

        # Convert video to data
        video_path = f'./user_data/{video_id}.mp4'
        with open(video_path, 'rb') as vid_file:
            video_data = conversion.convert_vid(vid_file, size=32, fps=15)  # Adjust size and fps if needed

        # Remove the video after conversion to avoid taking up space
        os.remove(video_path)

        return video_data
    except Exception as e:
        return f"Error downloading or converting video: {str(e)}"


# Search for YouTube videos
def search_youtube(query):
    try:
        videosSearch = VideosSearch(query, limit=6)
        result = videosSearch.result()

        # Prepare a list of video data
        video_list = []
        for video in result["result"]:
            video_data = {
                "title": video.get("title"),
                "publishedTime": video.get("publishedTime"),
                "duration": video.get("duration"),
                "views": video.get("viewCount", {}).get("text"),
                "thumbnail": video.get("thumbnails", [{}])[0].get("url"),
                "url": video.get("link")
            }
            video_list.append(video_data)

        return video_list
    except Exception as e:
        return f"Error searching YouTube: {str(e)}"
