import pyascii
from datetime import datetime

x = pyascii.Pyascii()
start = datetime.now()
# Render the video at 30 frames
fps = 30 if x.get_mp4_fps("GB.mp4") == 29 else x.get_mp4_fps("GB.mp4")
x.render_video(
    fps,
    "GB.mp4",
    "img/",
    "audio/gb_AUDIO.wav",
    "gb_NEW.mp4",
    "final.mp4"
)
print(f"Time: {datetime.now() - start}")
