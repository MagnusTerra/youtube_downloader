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
        
        
def download_just_video(url):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]',
        'outtmpl': '%(title)s.%(ext)s',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
    except Exception as e:
        print(f"An error ocurred during download: {e}")
        return
    finally:
        print("Download finished")
        
def download_video_audio(url):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': '%(title)s.%(ext)s',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
    except Exception as e:
        print(f"An error ocurred during download: {e}")
        return
    finally:
        print("Download finished")
        
#Download a play list and create a dor with the name of the playlist
def download_playlist(url, output_dir: str = None):
    """
    Downloads a YouTube playlist given its URL.

    Args:
        url (str): The URL of the YouTube playlist.
        output_dir (str, optional): The directory where the downloaded files will be saved. If not provided, the files will be saved in the current directory.

    Returns:
        None

    Raises:
        Exception: If an error occurs during the download.

    """
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': '%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s',
    }
    if output_dir is not None:
        ydl_opts['outtmpl'] = output_dir + '/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s'
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
    except Exception as e:
        print(f"An error occurred during download: {e}")
        return
    finally:
        print("Download finished")