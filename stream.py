 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/stream.py b/stream.py
index 626f98807b2d1088d93f8c1c83987a48d9a0884f..c3bfac188891d8d02ed36a5d0ca232dd025e9575 100644
--- a/stream.py
+++ b/stream.py
@@ -1,32 +1,87 @@
-import subprocess
 import os
+import subprocess
+import sys
+import time
+from pathlib import Path
+
+INPUT_FILE = Path("sleep_loop.mp4")
+NORMALIZED_FILE = Path("stream_ready.mp4")
+ENDPOINTS = [
+    "rtmps://a.rtmp.youtube.com:443/live2",
+    "rtmp://a.rtmp.youtube.com/live2",
+]
+
+
+def run(cmd):
+    print("+", " ".join(cmd), flush=True)
+    return subprocess.run(cmd)
+
+
+def fail(msg: str) -> None:
+    print(f"ERROR: {msg}", flush=True)
+    sys.exit(1)
+
+
+def get_stream_key() -> str:
+    raw = os.getenv("YOUTUBE_STREAM_KEY", "")
+    key = raw.replace("\r", "").replace("\n", "").strip()
+    if not key:
+        fail("YOUTUBE_STREAM_KEY secret is missing/empty")
+    if " " in key:
+        fail("YOUTUBE_STREAM_KEY contains spaces; paste only raw key")
+    print(f"INFO: stream key loaded (length={len(key)})", flush=True)
+    return key
 
-def start_stream():
-    stream_key = os.getenv('YOUTUBE_STREAM_KEY')
-    # Use the RTMPS URL for a more secure and stable connection
-    rtmp_url = f"rtmps://a.rtmp.youtube.com:443/live2/{stream_key}"
-    
-    # This command uses a reliable test video to ensure we get a picture
+
+def validate_input() -> None:
+    if not INPUT_FILE.exists():
+        fail("sleep_loop.mp4 was not found")
+
+    p = run(["ffprobe", "-v", "error", "-show_format", "-show_streams", str(INPUT_FILE)])
+    if p.returncode != 0:
+        fail("sleep_loop.mp4 is unreadable/corrupted")
+
+
+def normalize_media() -> None:
+    # Create a clean, stable MP4 with H.264 + AAC.
+    # If source has no audio, add silent stereo track.
     cmd = [
-        'ffmpeg',
-        '-re',
-        '-stream_loop', '-1',
-        '-i', 'video.mp4',
-        '-c:v', 'libx264',
-        '-preset', 'veryfast',
-        '-b:v', '3000k',
-        '-maxrate', '3000k',
-        '-bufsize', '6000k',
-        '-pix_fmt', 'yuv420p',
-        '-g', '60',
-        '-c:a', 'aac',
-        '-b:a', '128k',
-        '-ar', '44100',
-        '-f', 'flv',
-        rtmp_url
+        "ffmpeg", "-y", "-v", "warning",
+        "-i", str(INPUT_FILE),
+        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
+        "-map", "0:v:0", "-map", "0:a?", "-map", "1:a",
+        "-c:v", "libx264", "-preset", "veryfast", "-r", "30", "-g", "60", "-pix_fmt", "yuv420p",
+        "-c:a", "aac", "-b:a", "128k", "-ar", "44100",
+        "-shortest", "-movflags", "+faststart",
+        str(NORMALIZED_FILE),
     ]
-    
-    subprocess.run(cmd)
+    p = run(cmd)
+    if p.returncode != 0:
+        fail("failed to normalize video/audio")
+
+
+def publish_forever(stream_key: str) -> None:
+    while True:
+        for endpoint in ENDPOINTS:
+            url = f"{endpoint}/{stream_key}"
+            print(f"INFO: publishing to {endpoint}", flush=True)
+            cmd = [
+                "ffmpeg", "-hide_banner", "-loglevel", "info",
+                "-re", "-stream_loop", "-1", "-i", str(NORMALIZED_FILE),
+                "-c", "copy",
+                "-f", "flv", url,
+            ]
+            code = run(cmd).returncode
+            print(f"WARN: ffmpeg exited with code {code}; retrying in 5s", flush=True)
+            time.sleep(5)
+
+
+def main() -> None:
+    key = get_stream_key()
+    validate_input()
+    normalize_media()
+    publish_forever(key)
+
 
 if __name__ == "__main__":
-    start_stream()
+    main()
 
EOF
)
