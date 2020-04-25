from gtts import gTTS
import os
import requests
import re
import json
import time
from concurrent.futures import ThreadPoolExecutor
import moviepy.video.fx.all as vfx
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
import glob
import random


def text_to_speech(file,file_name,part_name,article,type_):
    language = 'en'
    print("waiting for file %s"%file_name)
    speech =gTTS(text = str(file), lang = language, slow = False)
    print("waiting is finiched")
    if type_ =="part":
        with open("../Articles/%s/audio/%s/%s.mp3"%(article,file_name,part_name), 'wb') as f:
            speech.write_to_fp(f)
    elif type_=="full":
        with open("../Articles/%s/audio/%s.mp3"%(article,file_name), 'wb') as f:
            speech.write_to_fp(f)
    elif type_ == "title":
        with open("../Articles/%s/audio/%s/title.mp3"%(article,file_name), 'wb') as f:
            speech.write_to_fp(f)

    print("file %s done"%file_name)
    

def prepare_content_to_text_to_speech_function(article_name):
    files =['intro']
    file = open("../Articles/%s/data.json"%article_name,"r")
    json_data = json.load(file)
    file.close()
    # ######## These 2 For are to create for each TOP an audio ########
    type_="full" # full means that this need to be saved in the audio folder not in the part folder of each TOP
    for i in range (10):
        print('starting file %s ...'%str(i+1))
        text_file  = json_data["video"][i+1]["content"].replace("\n"," ")
        text_to_speech(text_file,str(i+1),None,article_name,type_)

    for file in files:
        print('starting file %s ...'%file)
        text_file  = json_data["video"][0]["content"].replace("\n"," ")
        text_to_speech(text_file,file,None,article_name,type_)

# ##################################################################### 

# ######## These 2 For are to create for each 12 words of a TOP an audio ########
    type_="part" # part means that this need to be saved in the part folder of each TOP
    for i in range (10):
        print('starting file %s ...'%str(i+1))
        for j in range(len(json_data["video"][i+1]["list_content"])):
            text_file  = json_data["video"][i+1]["list_content"][j].replace("\n"," ")
            text_to_speech(text_file,str(i+1),str(j+1),article_name,type_)

    for i,file in enumerate(files):
        print('starting file %s ...'%file)
        for j in range(len(json_data["video"][0]["list_content"])):
            text_file  = json_data["video"][0]["list_content"][j].replace("\n"," ")
            text_to_speech(text_file,file,str(j+1),article_name,type_)
        
##################################################################### 

# ######## These For is to create for each Title an audio ########
    type_="title" # title means that this need to be saved in the part folder of each TOP as a title
    for i in range (10):
        print('starting file %s ...'%str(i+1))
        title_file  = json_data["video"][i+1]["title"].replace("\n"," ")
        modified_title = title_file.split(" ")
        modified_title[0] = 'Number %s...'%str(i+1)
        modified_title = ' '.join(modified_title)
        text_to_speech(modified_title,str(i+1),None,article_name,type_)

# ##################################################################### 


def edit_video(article_name):
    file = open("../Articles/%s/data.json"%article_name,"r")
    json_data = json.load(file)
    file.close()
    i=1
    file_name = i
    path ="../Articles/%s/audio/%s.mp3"%(article_name,str(i))
    images=glob.glob("../Articles/%s/%s/images/*"%(article_name,str(i)))
    videos=glob.glob("../Articles/%s/%s/videos/*"%(article_name,str(i)))
    title= json_data["video"][file_name]["title"].replace("\n"," ")
    #prepare subtitle
    generator = lambda txt: TextClip(txt, font='DejaVu-Sans-Bold', fontsize=40, color='white')
    subtitles = SubtitlesClip("../Articles/%s/%s/content.srt"%(article_name,str(i)), generator)
    title_duration= float(json_data["video"][file_name]["title_duration"])
    content_duration = float(json_data["video"][file_name]["content_duration"])
    #now we need to devide content duration over images and videos
    media_duration = float(content_duration/(len(images)+len(videos))) # means photo or video duration
    video_clips=[]
    for video in videos:
        video_clips.append(VideoFileClip(video).subclip(0,media_duration))
    image_clips=[]
    for image in images:
        image_clips.append(ImageClip(image).set_duration(media_duration))

    content_list=image_clips
 
    for video in video_clips:
         content_list.insert(random.randint(0,len(image_clips)-1),video)
    print(content_list)
    content_clip = concatenate_videoclips(content_list)
    content_audio_path = "../Articles/%s/audio/%s.mp3"%(article_name,str(i))
    content_clip.set_audio(AudioFileClip(content_audio_path))
    content_final= CompositeVideoClip([content_clip, subtitles.set_pos(('center','bottom'))])

    #create the title
    title_text_clip = TextClip('%s'%(modified_title),color='white', font="DejaVu-Sans-Bold",fontsize=60,size=(1920,1080)).set_pos('center')
    title_text_clip =title_text_clip.set_duration(title_duration)
    title_audio_path = "../Articles/%s/audio/%s/title.mp3"%(article_name,str(i))
    title_clip= title_text_clip.set_audio(AudioFileClip(title_audio_path))


    final_video = concatenate_videoclips([title_clip,content_clip])
    final_video.write_videofile("test.mp4",fps=25)



def init(article_name):
    print("processing...")
    # prepare_content_to_text_to_speech_function(article_name)
    edit_video(article_name)




init('Top 10 TV Shows Cancelled Too Soon')



