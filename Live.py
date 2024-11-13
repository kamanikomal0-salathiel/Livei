import subprocess
import os
import time

# YouTube Stream Key and Main RTMP URL
YOUTUBE_STREAM_KEY = "aw3v-q7qm-tcs5-m57b-4tf7"
YOUTUBE_RTMP_URL = f"rtmp://a.rtmp.youtube.com/live2/{YOUTUBE_STREAM_KEY}"
YOUTUBE_BACKUP_RTMP_URL = "rtmp://b.rtmp.youtube.com/live2?backup=1"

# File with video URLs
video_links_file = "video_links.txt"

# Check if the video links file exists
if not os.path.exists(video_links_file):
    print(f"Error: {video_links_file} not found. Please create it and add video URLs.")
    exit(1)

# Infinite loop for continuous streaming
while True:
    with open(video_links_file, "r") as file:
        video_links = file.readlines()

    for video_url in video_links:
        video_url = video_url.strip()
        if not video_url:
            continue

        # Step 1: Download the video
        video_file = "A.mp4"
        print(f"Downloading video from {video_url}...")
        try:
            subprocess.run(["wget", "-O", video_file, video_url], check=True)
        except subprocess.CalledProcessError:
            print(f"Error downloading video from {video_url}. Skipping...")
            continue

        # Step 2: Stream the video using FFmpeg
        ffmpeg_command = [
            "ffmpeg",
            "-re",  # Real-time streaming
            "-i", video_file,  # Input video file
            "-vf", "scale=720:1280",  # Resize to 9:16 aspect ratio (720x1280)
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
            print(f"Starting live stream for {video_file}...")
            subprocess.run(ffmpeg_command, check=True)
        except subprocess.CalledProcessError:
            print("Error during streaming. Retrying with backup URL...")
            ffmpeg_command[-1] = YOUTUBE_BACKUP_RTMP_URL
            subprocess.run(ffmpeg_command)

        # Step 3: Clean up the downloaded video
        if os.path.exists(video_file):
            os.remove(video_file)
            print(f"Cleaned up {video_file}.")

    # Optional: Wait before restarting the loop
    print("Waiting for 10 seconds before restarting...")
    time.sleep(10)
