import yt_dlp
import subprocess
import os

def sanitize_filename(filename):
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    return filename

def download_youtube_video(url):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': 'outputvideo.mp4',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_title = info_dict.get('title', 'outputvideo.mp4')

    return {"video_in":"outputvideo.mp4",
            "video_out":video_title}

def encode_video(video_in, video_out):
    #command = f"ffmpeg -i {video_in} -c:v libx264  -preset ultrafast -c:a aac -strict experimental {video_out}.mp4"
    video_out = sanitize_filename(video_out)
    try:
        subprocess.run([
                'ffmpeg', '-i', video_in, '-c:v', 'libx264', '-preset', 'ultrafast', '-c:a', 'aac', video_out + ".mp4"
            ], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"An error ocurred during transcoding: {e}")
    finally:
        print("Transcoding finished")
        os.remove(video_in)
        #os.rename("cosa.mp4", str(video_out) + ".mp4")