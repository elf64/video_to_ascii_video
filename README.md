# Video to ASCII Video
## Version 0.1
This is a simple video to ascii video renderer made in python... It's slow but it works :)
### Libraries it's using
1. python-opencv
2. PIL
### How it works
* ##### This currently works only on linux!
* We're first getting the audio from the original file then we start to get every frame from the original video.
* After we got every frame (we save it in the img folder) we start to render it in ascii
* Then we convert every frame to mp4 (without audio) and then we make the final one with audio
* We're using ffmpeg to get the audio, convert the frames to mp4 and add the audio to the final mp4
### Example
```python
import pyascii

render = pyascii.Pyascii()
fps = render.get_mp4_fps('/path/to/mp4/video.mp4')
render.render_video(
    fps,                                # Get the fps of the original video
    '/path/to/mp4/video.mp4',           # Path to the video we want to render
    'img/',                             # Path where to save the frames
    'audio/test.wav',                   # Path where to save the audio wav
    '/path/to/mp4/video_no_audio.mp4',  # Path where to save the final video without audio
    '/path/to/mp4/final_video.mp4'      # Path where to save the final video with audio
)
```
### Bugs
Try to always delete the old frames from img/ and old audio files from audio/
