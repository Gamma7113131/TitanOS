from moviepy.editor import VideoFileClip
from PIL import Image
from io import BytesIO
import cv2
import numpy as np
import os
import random


def rgb_to_number(rgb):
	r, g, b = rgb
	return r * 256**2 + g * 256 + b

def convert_img(img, size):
	resized_img = img.resize((size, size))
	image_data = []
	for y in range(size):
		row = []
		for x in range(size):
			rgb = resized_img.getpixel((x, y))[:3]
			row.append(rgb_to_number(rgb))
		image_data.append(row)
	return image_data

def convert_vid(vid, size, fps):
	video_path = f"temp_{random.randint(000,999)}.mp4"
	with open(video_path, 'wb') as video_file:
		for chunk in video_response.iter_content(chunk_size=8192):
			video_file.write(chunk)
	video_clip = VideoFileClip(video_path)
	resized_clip = video_clip.resize((size, size)).set_fps(fps)
	frames_data = []
	for frame in resized_clip.iter_frames(fps=fps,dtype="uint8"):
		pil_image = Image.fromarray(frame)
		frame_data = convert_img(pil_image)
		frames_data.append(frame_data)
		
	video_clip.close()
	resized_clip.close()
	os.remove(video_path)
	return frames_data