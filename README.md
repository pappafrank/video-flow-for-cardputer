# PixelFlow FW Video Formatter & Uploader

The videoplayer fw on cardputer really fked my head trying to make it work then i found this fw and make this automation. Special thanks to the contributer of PixelFlow @7h30th3r0n3
Turn any MP4 video into a flowing animation on your **M5 PixelFlow** device — automatically.

This tool:
1. Extracts frames from a video at selected fps (10-20 is recommended you can make it higher for shorter videos)  
2. Resizes them to **240×135** (stretched if needed)  
3. Uploads them safely to your PixelFlow’s local webserver (`http://192.168.4.1/upload`)

---

## Requirements

- Python 3.8 or newer  
- FFmpeg installed (`ffmpeg -version` should work)  
- M5 device running the PixelFlow firmware  
- Your computer connected to the **PixelFlow** Wi-Fi access point

Installation one-liner:
You can start by downloading the video you want (average 30 seconds is recommended). Then open the PixelFlow firmware on your cardputer and connect to the access point before executing the python file.
```bash

$ sudo apt install yt-dlp -y; git clone http://github.com/pappafrank/video-flow.git; cd video-flow; python3 -m venv venv;source venv/bin/activate; pip install -r requirements.txt; python3 video-flow.py
```


## Note

This is still really inconvinient for videos longer than 30 seconds so im working on another firmware to either play videos live from a device or use .mjpg etc. if you want to help me building this you can email ``` cetteviee@proton.me  ```
