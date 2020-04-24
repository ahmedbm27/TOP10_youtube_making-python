from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip

generator = lambda txt: TextClip(txt, font='DejaVu-Sans-Bold', fontsize=40, color='white')
subtitles = SubtitlesClip("test58.srt", generator)

video = VideoFileClip("1.mp4")
result = CompositeVideoClip([video, subtitles.set_pos(('center','bottom'))])

result.write_videofile("titi.mp4",fps=25)