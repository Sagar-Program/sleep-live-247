 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/README.md b/README.md
index 8f410cc9225e4c95f52b4083ed8fb7708b14f502..2698b1dc6f955ff2503629217b3295431f5d1111 100644
--- a/README.md
+++ b/README.md
@@ -1,2 +1,65 @@
-# sleep-live-247
-sleep-live-247
+# YouTube 24/7 Stream (sleep_loop.mp4)
+
+This setup is built for reliability with a single local file: `sleep_loop.mp4`.
+
+## What you must keep in repo
+- `sleep_loop.mp4` in repo root
+- `stream.py`
+- `.github/workflows/main.yml`
+
+## One-time setup
+1. Open your repo on GitHub.
+2. Go to **Settings → Secrets and variables → Actions**.
+3. Create secret:
+   - Name: `YOUTUBE_STREAM_KEY`
+   - Value: paste only the stream key (no URL, no spaces).
+
+## Run stream
+1. Open **Actions** tab.
+2. Click workflow **YouTube 24x7 Stream**.
+3. Click **Run workflow**.
+4. Open logs and confirm `INFO: publishing to ...` appears.
+
+## YouTube Live Control Room settings
+- Stream type: **Streaming software**
+- Auto-start: **ON**
+- Auto-stop: **OFF**
+- DVR: **ON**
+- Latency: **Normal**
+
+## Why this is stable
+- Validates MP4 before streaming (`ffprobe`).
+- Normalizes file to H.264 + AAC with silent fallback audio.
+- Tries RTMPS first, then RTMP fallback.
+- Auto-retries forever if FFmpeg exits.
+
+## Important truth about 24/7
+GitHub-hosted runners stop around 6 hours max per job.
+For true nonstop 24/7, run this exact repo on a **self-hosted runner** (your laptop/PC/VPS always on).
+
+
+## If your repository is empty (no files visible)
+
+This usually means one of these:
+- You are looking at a different GitHub repository than this code branch
+- You are on a different branch in GitHub UI
+- Local files were not pushed to GitHub yet
+
+### Send files to GitHub using browser (no terminal)
+1. Open your repo on GitHub.
+2. Click **Add file** → **Upload files**.
+3. Upload these from your laptop:
+   - `sleep_loop.mp4`
+   - `stream.py`
+4. Create folders in upload path for workflow:
+   - `.github/workflows/main.yml`
+5. Add commit message and click **Commit changes**.
+
+### Send files to GitHub using git (terminal)
+```bash
+git add .
+git commit -m "Add YouTube streaming files"
+git push origin <your-branch>
+```
+
+After upload/push, refresh your repo page and you should see files.
 
EOF
)
