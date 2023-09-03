from PIL import Image, ImageDraw, ImageFont
from IPython.display import display
import os
import random
import numpy as np
import shutil
import textwrap
import subprocess
import cv2
import os
import glob
import time
from moviepy.editor import *
from moviepy.video.fx import all
import textwrap
from moviepy.editor import VideoFileClip, VideoClip, CompositeVideoClip, concatenate_videoclips, concatenate_audioclips
import subprocess
import cv2
import os
import glob
import time
from PIL import Image, ImageDraw, ImageFont
from IPython.display import display
from pathlib import Path

# instraction for video bulk video creation
#instagram reels size 1080 * 1920 px
#instagram reels duration 5sec

class VideoGen:
    def __init__(self) -> None:
        Path("temp").mkdir(exist_ok= True)
        self.font_name_hindi = "/home/kali/Desktop/instagram/font/NotoSansDevanagari-Black.ttf"
        self.font_name_eng = "/home/kali/Desktop/instagram/font/Freedom45.ttf"
        self.font_name_eng_bold = "/home/kali/Desktop/instagram/font/eng.otf"
        self.output_size = (1080, 1920)
        self.background_image = None
        self.total_duration = 5
        self.fps = 10
        self.width = 1080
        self.height = 1920
        self.background_color = (0, 0, 0, 0)
        self.const_top_padding = 30
        self.max_line_width = 60
        self.font_scale = 4.0
        self.thickness = 6
        self.color_black = (0, 0, 0)
        self.color_red = (255, 0, 0, 255)
    @property
    def getHindiFont(self):
        return self.font_name_hindi
    @property
    def getEngFont(self):
        return self.font_name_eng
    @property
    def getEngBoldFont(self):
        return self.font_name_eng_bold
    @property
    def getBackgroundImage(self):
        background_image = ImageClip(random.choice([i for i in glob.glob('backgrounds/*')]))
        return background_image
    @property
    def getGifImage(self):
        baby_gif = random.choice([i for i in glob.glob("gif/*.gif")])
        return baby_gif
    @property
    def getAudioFile(self):
        audio_path = random.choice([i for i in glob.glob("voice/*")])
        audio_clip = AudioFileClip(audio_path)
        video_duration = 5  # Desired video duration in seconds
        num_repeats = int(video_duration / audio_clip.duration) + 1
        repeated_clips = [audio_clip.copy() for _ in range(num_repeats)]
        looped_audio = concatenate_audioclips(repeated_clips)
        return looped_audio , audio_clip.duration
    def make_frame(self,t):
        return self.background_image.get_frame(t)
    def apply_shaking_effect(self,frame):
        # Define shaking parameters (adjust as needed)
        intensity = 3  # Intensity of the shaking
        offset_x = random.randint(-intensity, intensity)
        offset_y = random.randint(-intensity, intensity)
        
        # Apply shaking effect to the frame
        shaken_frame = np.roll(frame, (offset_y, offset_x), axis=(0, 1))
        return shaken_frame
    def genBackgroundVideo(self, audio_clip):
        background_image = self.getBackgroundImage
        self.background_image = background_image.resize(self.output_size)
        video_clip = VideoClip(self.make_frame, duration=self.total_duration)
        video_with_audio = video_clip.set_audio(audio_clip)
        return video_with_audio
    def logoRender(self,):
        font = ImageFont.truetype(self.getEngFont, 37, layout_engine=ImageFont.TransposedFont,)
        image = Image.new("RGBA", (self.width, self.height), self.background_color)
        draw = ImageDraw.Draw(image)
        text = "@heyitsmeraaj"
        lines = textwrap.wrap(text, width=50)
        y = 200 + self.const_top_padding 
        for line in lines:
            text_width, text_height = 50, 0
            x = (self.width - text_width) / 2 -200
            draw.text((x,y), line, font=font, fill=(255, 0, 0, 255), bold=True)
            y += int(self.font_scale * 20)  # adjust the spacing between lines as needed
            image.save(f"temp/1.png")
    def contains_hindi_characters(self, word):
        for char in word:
            if 0x0900 <= ord(char) <= 0x097F:
                return True
        return False
    def textRender(self, text, filename, position_y):
        """Render text using different fonts for Hindi and English characters.

        Args:
            text (str): The input text containing Hindi and English characters.
            filename (str): The filename to save the output image.
            position_y (int): The vertical position of the first line of text.
        """
        image = Image.new("RGBA", (self.width, self.height), self.background_color)
        draw = ImageDraw.Draw(image)
        lines = textwrap.wrap(text, width=40)
        y = position_y + self.const_top_padding
        isHighlight = True
        highlightWord = ["दूध", "थक","नागिन,"]

        for line in lines:
            text_width, text_height = 40, 0
            line_width = self.get_line_width(line)
            x = (self.width - line_width) / 2  # Center the line horizontally
            for char in line.split(" "):
                char_width = self.get_char_width(char)
                if not self.contains_hindi_characters(char):  # English character
                    font_name = self.getEngBoldFont
                    font = ImageFont.truetype(font_name, 30, layout_engine=ImageFont.TransposedFont)
                    char = char + " "
                    draw.text((x, y), char, font=font, fill=self.color_red, bold=True)
                else:  # Hindi character
                    font_name =  self.getHindiFont
                    font = ImageFont.truetype(font_name, 50, layout_engine=ImageFont.TransposedFont)
                    char = char + " "
                    if isHighlight == True and char in [i+" " for i in highlightWord]:
                        draw.text((x, y), char, font=font, fill=self.color_red, bold=True)
                    else:
                        draw.text((x, y), char, font=font, fill=(0, 0, 0), bold=True)
                x += char_width
            y += int(self.font_scale * 20)  # Adjust the spacing between lines as needed
        image.save("temp/{}.png".format(filename))
        return y
    def get_char_width(self, char):
        font_name = self.getEngBoldFont if not self.contains_hindi_characters(char) else self.getHindiFont
        font_size = 30 if not self.contains_hindi_characters(char) else 50
        font = ImageFont.truetype(font_name, font_size, layout_engine=ImageFont.TransposedFont)
        char_width = font.getlength(char + " ")
        return char_width

    def get_line_width(self, line):
        return sum([self.get_char_width(char) for char in line.split(" ")])

    
    def getemojiImage(self, filename, y_position):
        emoji = [Image.open(i) for i in glob.glob("emoji/*")]
        random.shuffle(emoji)
        emoji = emoji[:6]
        total_width = sum(image.width for image in emoji)
        max_height = max(image.height for image in emoji)
        desired_size = (100, 100)  # Replace with the size you want
        emoji = [Image.open(i).resize(desired_size) for i in glob.glob("emoji/*")]
        total_width = sum(image.width for image in emoji)
        max_height = desired_size[1]
        joined_image_horizontal = Image.new("RGBA", (self.width, self.height), self.background_color)
        x_position = 260
        for image in emoji:
            joined_image_horizontal.paste(image, (x_position, y_position))
            x_position += image.width
        # Save the joined image
        joined_image_horizontal.save("temp/{}.png".format(filename))
    def get_gif_duration(self, gif_path):
        gif = Image.open(gif_path)
        # Get the duration of the GIF in milliseconds (ms)
        duration = gif.info.get('duration')
        # Close the image
        gif.close()
        return duration / 1000.0  # Convert duration to seconds
    
    def getGifClip(self):
        gif_path = self.getGifImage
        gif_clip = VideoFileClip(gif_path,  has_mask=True,).loop().resize((400,300))
        gif_position = ('center', 'center')
        gif_clip = gif_clip.set_position(gif_position).set_duration(self.total_duration)
        return gif_clip
    
    def getImageClip(self, filename):
         return ImageClip("temp/{}.png".format(filename)).set_duration(self.total_duration)
    def getVideoShaking(self, final_video, audio_clip, audio_duration):
        frames = [final_video.get_frame(t) for t in np.arange(0, self.total_duration, 1/self.fps)]
        shaken_frames = [self.apply_shaking_effect(frame) for frame in frames]
        shaken_video_clip = VideoClip(make_frame=lambda t: shaken_frames[int(t * self.fps)], duration=self.total_duration)
        if audio_duration >3 and audio_duration <= 5:
            shaken_video_with_audio = (shaken_video_clip.set_audio(audio_clip).subclip(0, audio_duration))
        else:
            shaken_video_with_audio = (shaken_video_clip.set_audio(audio_clip).subclip(0, 5))
        return shaken_video_with_audio
    def cleanData(self):
        shutil.rmtree("temp")
        
if __name__ == "__main__":
    
    text1 = "कुत्ता पाल लेना, शेर पाल लेना और घोडा भी पाल लेना.."
    text2 = "पर ये वहम मत पालना  की लव मैरिज के बारे में बताओगे और घर वाले मान जायेंगे"
    obj = VideoGen()
    video_with_gif_clip = obj.getGifClip()
    obj.logoRender()
    obj.textRender(text=text1 , filename="2", position_y= 400)
    y_position = obj.textRender(text=text2 , filename="3", position_y= 1200)
    obj.getemojiImage("4", y_position= y_position)
    audio_clip , audio_duration = obj.getAudioFile
    video_with_audio = obj.genBackgroundVideo(audio_clip= audio_clip)

    video_with_gif_clip = obj.getGifClip()
    logo_text_clip = obj.getImageClip("1")
    text1_clip = obj.getImageClip("2")
    text2_clip = obj.getImageClip("3")
    emoji_clip = obj.getImageClip("4")
    final_video = CompositeVideoClip([video_with_audio, video_with_gif_clip, logo_text_clip, text1_clip, text2_clip, emoji_clip])
    
    shaken_video_with_audio = obj.getVideoShaking(final_video= final_video , audio_clip= audio_clip , audio_duration= audio_duration)
 
    output_file = 'output_image_background.mp4'
    shaken_video_with_audio.write_videofile(output_file, codec='libx264', audio_codec='aac', fps=10)
    obj.cleanData()
