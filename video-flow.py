import cv2
import os
import ffmpeg
import time
import requests
from tqdm import tqdm
import json

print(r"""
        _     __                 ______             
 _   __(_)___/ /__  ____        / __/ /___ _      __
| | / / / __  / _ \/ __ \______/ /_/ / __ \ | /| / /
| |/ / / /_/ /  __/ /_/ /_____/ __/ / /_/ / |/ |/ / 
|___/_/\__,_/\___/\____/     /_/ /_/\____/|__/|__/

                                        by pappa \n
""")
VIDEO_PATH = input("Video path: ")
OUTPUT_DIR = "frames"
TARGET_FPS = input("FPS (10-20 is recommended): ")
FRAME_WIDTH = 240
FRAME_HEIGHT = 135
SERVER_URL = "http://192.168.4.1/upload"
DELAY_BETWEEN_UPLOADS = input("Delay between uploads(1.0-2.0 is recommended): ")
JPEG_QUALITY = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

def extract_frames(video_path, output_dir, fps):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    (
        ffmpeg
        .input(video_path)
        .output(f"{output_dir}/frame_%05d.jpg", r=fps, qscale=2)
        .run(overwrite_output=True, quiet=True)
    )
    print(f"Frames extracted to '{output_dir}'")

def resize_frames(folder, width, height):
    files = sorted([f for f in os.listdir(folder) if f.lower().endswith(".jpg")])
    for f in tqdm(files, desc="Resizing frames"):
        path = os.path.join(folder, f)
        img = cv2.imread(path)
        if img is None:
            continue
        resized = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
        cv2.imwrite(path, resized, JPEG_QUALITY)
    print(f"All frames resized to {width}x{height}")


def upload_frames(folder, server_url, delay):
    files = sorted([f for f in os.listdir(folder) if f.lower().endswith(".jpg")])
    total = len(files)
    print(f"Uploading {total} frames to {server_url}...")

    for f in tqdm(files, desc="Uploading"):
        path = os.path.join(folder, f)
        try:
            with open(path, "rb") as img_file:
                files_dict = {"data": (f, img_file, "image/jpeg")}
                response = requests.post(server_url, files=files_dict, timeout=30)
                if response.status_code != 200:
                    print(f"Upload failed for {f} (HTTP {response.status_code})")
        except Exception as e:
            print(f"Error uploading {f}: {e}")

        time.sleep(delay)

    print("Upload completed!")

import json

def update_m5_interval(server_base_url, video_path):
    """Automatically update the M5's image change interval to match the video FPS."""
    probe = ffmpeg.probe(video_path)
    fps_str = probe['streams'][0]['r_frame_rate']
    fps = eval(fps_str)  # e.g., "30/1" -> 30.0

    interval_ms = int(1000 / fps)
    print(f"Video FPS detected: {fps:.2f} → Setting interval to {interval_ms} ms")

    try:
        response = requests.post(
            f"{server_base_url}/update-settings",
            data={"interval": str(interval_ms)},
            timeout=10
        )
        if response.status_code == 200:
            print("M5 interval updated successfully.")
        else:
            print(f"Failed to update interval (HTTP {response.status_code})")
    except Exception as e:
        print(f"Error updating interval: {e}")

    return interval_ms


if __name__ == "__main__":
    print("Extracting frames from video...")
    extract_frames(VIDEO_PATH, OUTPUT_DIR, TARGET_FPS)

    print("Resizing frames...")
    resize_frames(OUTPUT_DIR, FRAME_WIDTH, FRAME_HEIGHT)

    update_m5_interval("http://192.168.4.1", VIDEO_PATH)

    print("Starting upload to PixelFlow server...")
    upload_frames(OUTPUT_DIR, SERVER_URL, DELAY_BETWEEN_UPLOADS)
