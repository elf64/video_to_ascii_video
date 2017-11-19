from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from datetime import datetime
import subprocess
import glob
import cv2

# Version 0.1


class Pyascii:
    def __init__(self):
        self.bg_color = 'black'
        self.default_chars = list('_^:-=fg#%@')
        self.font = 'Anonymous_Pro.ttf'
        self.char_brightness_list = self.char_brightness()

    def avg_brightness_pixel(self, r, g, b):
        # Returns the average brightness value of a pixel
        return (r + g + b) / 3

    def render_image(
            self,
            image_path,
            save_path,
            show=None,
            save=None,
            enh_color=None,
            enh_brg=None,
            optimize=False,
            quality=100
    ):
        # Default function to convert an image to a ascii image
        image = Image.open(image_path)
        w, h = image.size
        block_size = int((w + h) / 200) - 2
        font_size = block_size + 4
        if w < 1024 and h < 768:
            block_size += 2
            font_size += 2
        font_l = ImageFont.load_default()
        rgb_image = image.convert('RGB')
        final_image = Image.new(rgb_image.mode, rgb_image.size, self.bg_color)
        draw = ImageDraw.Draw(final_image)
        for i in range(0, w, block_size):
            for j in range(0, h, block_size):
                color = (r, g, b) = rgb_image.getpixel((i, j))
                avg_brg = (r + g + b) / 3
                self.draw_text(self.default_chars[self.check_loop(avg_brg)]
                        ,draw, i, j, font_l, color)
        # Check for the other arugments
        final_image = ImageEnhance.Color(final_image).enhance(enh_color) \
        if enh_color != None else final_image
        final_image = ImageEnhance.Brightness(final_image).enhance(enh_brg)\
        if enh_brg   != None else final_image
        final_image.show() \
        if show != None else 0 
        final_image.save(save_path,optimize=optimize,quality=quality) \
        if save != None else 0  

    def render_video(self, fps, mp4_path, frame_path, audio_path, out_path, final):
        # fps           - Frame rate of the video
        # mp4_path      - Path to mp4
        # frame_path    - Path to frames
        # audio_path    - Path to audio
        # out_path      - Path to the final ascii video (without audio)
        # final         - Path to the fianl ascii video (with audio)
        self.get_mp4_audio(mp4_path, audio_path)
        self.get_video_frame(mp4_path, frame_path)
        self.render_frames(frame_path)
        self.make_mp4(frame_path, out_path, fps)
        self.add_audio(out_path, audio_path, final)
   
    def add_audio(self, mp4_path, wav_path, out_path):
        # Add audio to a mp4 file
        command = f'ffmpeg -i {mp4_path} -i {wav_path} -c:v copy -map 0:v:0 -map 1:a:0 -c:a aac -b:a 192k {out_path}'.split(' ')
        subprocess.check_output(command)

    def make_mp4(self, frame_path, mp4_path, fps):
        # Make a mp4 file from a bunch of images
        command = f'ffmpeg -f image2 -r {fps} -i {frame_path}/frame%7d.jpg -vcodec mpeg4 -y {mp4_path}'.split(' ')
        subprocess.check_output(command)

    def render_frames(self, frame_path):
        # Render the frames in ascii
        frame_len = len(glob.glob(f'{frame_path}/*.jpg'))
        print(f'Rendering {frame_len} frames...')
        for i in range(frame_len-1):
            start = datetime.now()
            self.render_image(
                    f'{frame_path}frame{i:07}.jpg',
                    f'{frame_path}frame{i:07}.jpg',
                    enh_color = 3.0,
                    enh_brg = 2.0,
                    save=1
            )

    def get_video_frame(self, mp4_path, frame_path):
        # Try to add the function in a thread and then kill it
        # when we get the first error.
        cap = cv2.VideoCapture(mp4_path)
        count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            cv2.imwrite(f'{frame_path}frame{count:07}.jpg', frame)
            count += 1
            cv2.waitKey(1)
            if cv2.waitKey(30) >= 0: break
            if ret == False: break
        print(f'frames : {count}')
        cap.release()

    def get_mp4_fps(self, mp4_path):
        cap = cv2.VideoCapture(mp4_path)
        return int(cap.get(cv2.CAP_PROP_FPS))

    def get_mp4_audio(self, mp4_path, wav_path):
        # Get the audio from a .mp4 file
        command = f'ffmpeg -i {mp4_path} -ab 160k -ac 2 -ar 44100 -vn {wav_path}'.split(' ')
        proc = subprocess.check_output(command)

    def check_loop(self, value):
        # We're doing a loop in range 10 (length of the ascii chars we use)
        # and it returns what index of the ascii character we need to use
        for i in range(len(self.default_chars)):
            if value < self.char_brightness_list[i]:
                return i
            elif (value >= self.char_brightness_list[i-1] and
                        value < self.char_brightness_list[i]):
                return i
            elif value == 255.0: return len(self.default_chars)-1

    def char_brightness(self):
        # Will return a list of all the brightness values for each character
        # in the charset
        amount_levels = len(self.default_chars)
        inner_list = []
        for i in range(amount_levels):
            level_brightness = (i + 1) * (255 / amount_levels)
            inner_list.append(level_brightness)
        return inner_list

    def draw_text(self, charx, draw, x, y, font, color):
        # Draw the char into the new image we created (self.final_image)
        # at x, y with the default font + default color
        return draw.text((x, y), charx, font=font, fill=color)

    def test(self):
        # Test function
        return "test"

