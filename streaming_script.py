import subprocess
import os

# YouTube Stream Key and Main RTMP URL
YOUTUBE_STREAM_KEY = "aw3v-q7qm-tcs5-m57b-4tf7"
YOUTUBE_RTMP_URL = f"rtmp://a.rtmp.youtube.com/live2/{YOUTUBE_STREAM_KEY}"

# Backup RTMP URL
YOUTUBE_BACKUP_RTMP_URL = "rtmp://b.rtmp.youtube.com/live2?backup=1"

# Video URL to download
VIDEO_URL = "https://download.bbupload.com/download.bbupload.com/682033/Animal.2023.1080p.CAMRip.TEL.DUB.1XBET.mkv"
VIDEO_FILE = "A.mp4"

def download_video():
    """Download the video using wget."""
    if os.path.exists(VIDEO_FILE):
        print(f"{VIDEO_FILE} already exists. Skipping download.")
    else:
        print(f"Downloading video from {VIDEO_URL}...")
        subprocess.run(["wget", "-O", VIDEO_FILE, VIDEO_URL], check=True)
        print(f"Video downloaded as {VIDEO_FILE}.")

def stream_video():
    """Stream the video using FFmpeg."""
    ffmpeg_command = [
        "ffmpeg",
        "-re",  # Real-time streaming
        "-stream_loop", "-1",  # Loop the video indefinitely
        "-i", VIDEO_FILE,  # Input video file
        "-vf", "scale=720:1280",  # Resize to 9:16 aspect ratio (720x1280 for Shorts)
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-b:v", "3000k",
        "-maxrate", "3000k",
        "-bufsize", "6000k",
        "-pix_fmt", "yuv420p",
        "-g", "50",
        "-c:a", "aac",
        "-b:a", "160k",
        "-ar", "44100",
        "-f", "flv",  # RTMP requires FLV format
        YOUTUBE_RTMP_URL
    ]

    try:
        print("Starting stream on main RTMP URL...")
        subprocess.run(ffmpeg_command, check=True)
    except subprocess.CalledProcessError:
        print("Main RTMP URL failed, switching to backup URL...")
        ffmpeg_command[-1] = YOUTUBE_BACKUP_RTMP_URL
        subprocess.run(ffmpeg_command)

def main():
    """Main function to download and stream the video."""
    while True:
        download_video()
        stream_video()
        print("Streaming completed. Restarting...")

if __name__ == "__main__":
    main()
