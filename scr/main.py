from fuctions import *

if __name__ == "__main__":
    youtube_url = input("Enter the YouTube URL: ")
    
    #youtube_url = "https://www.youtube.com/watch?v=BaW_jenozKc"
    video_name, video_end = download_youtube_video(youtube_url).values()
    
    encode_video(video_name, video_end)
    
    print(f"Video '{video_end}' downloaded as {video_name}")
