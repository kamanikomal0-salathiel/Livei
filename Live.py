import subprocess

# YouTube Stream Key and Main RTMP URL
YOUTUBE_STREAM_KEY = "aw3v-q7qm-tcs5-m57b-4tf7"
YOUTUBE_RTMP_URL = f"rtmp://a.rtmp.youtube.com/live2/{YOUTUBE_STREAM_KEY}"

# Backup RTMP URL
YOUTUBE_BACKUP_RTMP_URL = "rtmp://b.rtmp.youtube.com/live2?backup=1"

# Video file path (vertical format or cropped)
video_file = "A.mp4"

# FFmpeg command for vertical/shorts format with loop enabled
ffmpeg_command = [
    "ffmpeg",
    "-re",  # Real-time streaming
    "-stream_loop", "-1",  # Loop the video indefinitely
    "-i", video_file,  # Input video file
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

# Start streaming to main RTMP URL
try:
    print("Starting stream on main RTMP URL...")
    subprocess.run(ffmpeg_command, check=True)
except subprocess.CalledProcessError:
    print("Main RTMP URL failed, switching to backup URL...")
    # Stream to backup RTMP URL if the main one fails
    ffmpeg_command[-1] = YOUTUBE_BACKUP_RTMP_URL
    subprocess.run(ffmpeg_command)
