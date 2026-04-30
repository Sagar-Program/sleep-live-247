import subprocess
import os

def start_stream():
    stream_key = os.getenv('YOUTUBE_STREAM_KEY')
    # Use the RTMPS URL for a more secure and stable connection
    rtmp_url = f"rtmps://a.rtmp.youtube.com:443/live2/{stream_key}"
    
    # This command uses a reliable test video to ensure we get a picture
    cmd = [
        'ffmpeg',
        '-re',
        '-stream_loop', '-1',
        '-i', 'video.mp4',
        '-c:v', 'libx264',
        '-preset', 'veryfast',
        '-b:v', '3000k',
        '-maxrate', '3000k',
        '-bufsize', '6000k',
        '-pix_fmt', 'yuv420p',
        '-g', '60',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-ar', '44100',
        '-f', 'flv',
        rtmp_url
    ]
    
    subprocess.run(cmd)

if __name__ == "__main__":
    start_stream()
