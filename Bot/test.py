import requests
import re
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import json
import time
import datetime
import moviepy.video.fx.all as vfx
from moviepy.editor import *
import glob
SECONDS_IN_HOUR = 3600
SECONDS_IN_MINUTE = 60
HOURS_IN_DAY = 24
MICROSECONDS_IN_MILLISECOND = 1000
test_sentence=""
article_name="Top 10 TV Shows Cancelled Too Soon"
file = open("../Articles/%s/data.json"%article_name,"r")
json_data = json.load(file)
file.close()   

start_time = datetime.timedelta(hours=0, minutes=0, seconds=0)
block_num =1

def time_addition(sentence,current_time,extra_avg,audio_path,save_path):# this function make srt file
#if it is string we cant add an int to string so we add ''
  sentence=sentence.split(" ")
  sentence.insert(6,"\n")
  sentence = ' '.join(sentence)
  audioclip = AudioFileClip(audio_path)
  time_add = audioclip.duration - extra_avg
  audioclip.close()
  end_time = current_time + datetime.timedelta(0,time_add)
  # print(timedelta_to_srt_timestamp(current_time))
  str_current_time = timedelta_to_srt_timestamp(current_time)
  str_end_time = timedelta_to_srt_timestamp(end_time)

  with open(save_path,"a+") as f:
    f.write(str(block_num))
    f.write("\n")
    f.write(str_current_time)
    f.write(" --> ")
    f.write(str_end_time)
    f.write("\n")
    f.write(sentence)
    f.write("\n")
    f.write("\n")
  return end_time
def timedelta_to_srt_timestamp(timedelta_timestamp): #this function return a string contain .srt file Time
    r"""
    Convert a :py:class:`~datetime.timedelta` to an SRT timestamp.

    .. doctest::

        >>> import datetime
        >>> delta = datetime.timedelta(hours=1, minutes=23, seconds=4)
        >>> timedelta_to_srt_timestamp(delta)
        '01:23:04,000'

    :param datetime.timedelta timedelta_timestamp: A datetime to convert to an
                                                   SRT timestamp
    :returns: The timestamp in SRT format
    :rtype: str
    """

    hrs, secs_remainder = divmod(timedelta_timestamp.seconds, SECONDS_IN_HOUR)
    hrs += timedelta_timestamp.days * HOURS_IN_DAY
    mins, secs = divmod(secs_remainder, SECONDS_IN_MINUTE)
    msecs = timedelta_timestamp.microseconds // MICROSECONDS_IN_MILLISECOND
    return "%02d:%02d:%02d,%03d" % (hrs, mins, secs, msecs)

# hedhy te7seblek average far9 fel wa9t mabin il audio file kamel wel total mta3 parts mta3 audio 
def get_extra_average(file_name,article_name):
  audios=glob.glob("../Articles/%s/audio/%s.mp3"%(article_name,file_name))
  audio_parts =glob.glob("../Articles/%s/audio/%s/*.mp3"%(article_name,file_name))
  audio_full = AudioFileClip(audios[0])
  audios_duration= audio_full.duration #hedhy duration mta3 full audio
  audio_full.close()
  # print(audios_duration)
  audio_parts_duration =0 # hedhy sum mta3 durations mta3 audio parts
  for audio in audio_parts:
    x=1
    audio_part= AudioFileClip(audio)
    audio_parts_duration += audio_part.duration
    audio_part.close()
  # print("%s"%audio_parts_duration)
  average = (audio_parts_duration-audios_duration)/len(audio_parts)
  # print(average)
  return average

def save_durations_json(file_name,full_audio_path,type_):
  audioclip = AudioFileClip(full_audio_path)
  if type_ =="content":
    json_data["video"][file_name]["content_duration"]=str(audioclip.duration)
  else:
    json_data["video"][file_name]["title_duration"]=str(audioclip.duration)
  audioclip.close()
  with open('../Articles/%s/data.json'%article_name,"w")   as file_json:
    json.dump(json_data,file_json) 

############ this is to make STR file for the TOP ############
for i in range (10):
    
    test_sentence  = json_data["video"][i+1]["list_content"]
    extra_avg=get_extra_average(i+1,article_name)
    for ind,line in enumerate(test_sentence):
      audio_path = "../Articles/%s/audio/%s/%s.mp3"%(article_name,str(i+1),str(ind+1))
      save_path = "../Articles/%s/%s/content.srt"%(article_name,str(i+1))
      start_time = time_addition(line.replace("\n",""),start_time,extra_avg,audio_path,save_path)
      block_num +=1
    full_audio_path = "../Articles/%s/audio/%s.mp3"%(article_name,str(i+1))
    save_durations_json(i+1,full_audio_path,"content")
# ############################################################

# ############ this is to make STR file for the intro,conclusion ############
block_num =1
test_sentence  = json_data["video"][0]["list_content"]
extra_avg=get_extra_average(json_data["video"][0]["title"],article_name)
for ind,line in enumerate(test_sentence):
  audio_path = "../Articles/%s/audio/%s/%s.mp3"%(article_name,json_data["video"][0]["title"],str(ind+1))
  save_path = "../Articles/%s/%s/content.srt"%(article_name,json_data["video"][0]["title"])
  start_time = time_addition(line.replace("\n",""),start_time,extra_avg,audio_path,save_path)
  block_num +=1
full_audio_path = "../Articles/%s/audio/%s.mp3"%(article_name,json_data["video"][0]["title"])
save_durations_json(0,full_audio_path,"content")
# ############################################################

############ this is to make STR file for the titles ############
block_num =1
for i in range (10):
    audio_path = "../Articles/%s/audio/%s/title.mp3"%(article_name,str(i+1))
    save_path = "../Articles/%s/%s/title.srt"%(article_name,str(i+1))
    test_sentence  = json_data["video"][i+1]["title"]
    extra_avg=0
    start_time = time_addition(test_sentence.replace("\n",""),start_time,extra_avg,audio_path,save_path)
    block_num +=1
    full_audio_path = "../Articles/%s/audio/%s/title.mp3"%(article_name,str(i+1))
    save_durations_json(i+1,full_audio_path,"title")
############################################################


#     print("doing file %s"%i)
# audios=glob.glob(r"..\Articles\Top 10 Unsolved Mysteries Of The COVID-19 Pandemic\audio\*")
# print(audios)
# for audio in audios:
#   audioclip = AudioFileClip(audio)
#   print("%s"%audioclip.duration)

# for i in range(11):
#   test_sentence = json_data["video"][i]["content"]
#   title=json_data["video"][i]["title"]
#   x= test_sentence.replace("\n"," ").split(" ")
#   ch=len(x)-1
#   for y in x:
#     ch += len(y)
#   print("title : %s . words : %s char : %s"%(title,len(x),ch))



def create_new_article(article_name,headers,article_text):
    files =['intro','conclusion','audio']

    #create Article Folder Name
    try:
        # Create target Directory
        os.mkdir('../Articles/%s'%article_name)
        print("Directory " , article_name ,  " Created ") 
    except FileExistsError:
        print("Directory " , article_name ,  " already exists")

    # create folders from 1 to 10 
    for i in range (10):
        try:
        # Create target Directory
            os.mkdir('../Articles/%s/%s'%(article_name,i+1))
            print("Directory " , i+1 ,  " Created ") 
        except FileExistsError:
            print("Directory " , i+1 ,  " already exists")
    # create folder intro conclusion and audio
    for file in files:
        try:
            # Create target Directory
            os.mkdir('../Articles/%s/%s'%(article_name,str(file)))
            print("Directory " , file ,  " Created ") 
        except FileExistsError:
            print("Directory " , file ,  " already exists")

        # create folders from 1 to 10 in audio file
    for i in range (10):
        try:
        # Create target Directory
            os.mkdir('../Articles/%s/audio/%s'%(article_name,i+1))
            print("Directory " , i+1 ,  " Created ") 
        except FileExistsError:
            print("Directory " , i+1 ,  " already exists")

    # create folder intro conclusion in audio file
    for i  in range (len(files)-1):
        try:
            # Create target Directory
            os.mkdir('../Articles/%s/audio/%s'%(article_name,str(files[i])))
            print("Directory " , files[i] ,  " Created ") 
        except FileExistsError:
            print("Directory " , files[i] ,  " already exists")
    json_data ={
    "video":[]
    }
    try:
      with open('../Articles/%s/data.json'%article_name,"a+")   as file_json:
        json.dump(json_data,file_json)
    except Exception as e:
      print(e)
    text_organizer(article_name,'intro',re.sub(r'\[.+?\]', '', article_text[0]),0)
    for i in range(10):
      text_organizer(article_name,headers[i],re.sub(r'\[.+?\]', '', article_text[i+1]),i+1)
    
  

def text_organizer(article_name,title,text,file_name):
  print('starting file %s ...'%str(file_name))
  Title=title#article title
  text_list=text.split(" ") # split the text content so we can devide it to 6 words per line
  file = open("../Articles/%s/data.json"%article_name,"r")
  json_data = json.load(file)
  file.close()
 
  json_data["video"].append({
  "name":"%s"%file_name,
  "title":"%s"%title,
  "content":"",
  "list_content":[],
  "title_duration":'',
  "content_duration":''
  })
  
  my_content_list=[' '.join(text_list[12 * i: 12 * i + 12]) for i in range(0, int(len(text_list) / 12))]
  number_of_extra_words=round(((len(text_list) / 12)-int(len(text_list) / 12))*12)+int(len(text_list) / 12)*12 # hedhi ta3tik number of words ili mezelou felekher
  
  extra_my_content_list=[' '.join(text_list[int(len(text_list) / 12)*12: number_of_extra_words])]
  
  for extra in extra_my_content_list: #hedhy bch nzidou il extra lel contnet
    my_content_list.append(extra) #hedhy bch to93ed list
  
  my_content = "\n".join(my_content_list) # hedhy to make a paragprah ( list to paragraph )

  for x in my_content_list:#hedhy bch nektbou il list fel lis_contnet fel json file
    json_data["video"][file_name]["list_content"].append(x)
  
  json_data["video"][file_name]["content"]= my_content #hedhy bch nektbou il paragraph lel Contnet fel json file

  with open('../Articles/%s/data.json'%article_name,"w")   as file_json:
    json.dump(json_data,file_json)  
  print("file %s done"%str(file_name))


def website_parser(url):
  driver = webdriver.Chrome("./chromedriver.exe")
  driver.get(url)
  soup =BeautifulSoup(driver.page_source, 'html.parser')
  title=soup.find_all('h1')[0].text
  author_bio = soup.find(class_="author-bio") #hedhi bch nchouf idha kan famma author bio DIV
  article_content = soup.find(id="articlecontentonly").find_all(["p","h2"])
  headers =[] # titles of each  TOP
  article_text =['','','','','','','','','','','']
  i= 0 # TOP number ie : TOP 1
  #remove all promote element ( trahs elments)

  counter = 0 
  extra_P =0
  for el in article_content:
    if el.has_attr('class') and el['class'][0] == 'promote_see_also':
      el.decompose()

    if el.text =='' :
      el.decompose()
    
    if el.text =='\n' :
      el.decompose()
    
  for idx,el in enumerate(article_content):
    if el.name == "h2":
      headers.append(el.text)
      i +=1
    elif el.name =="p":
      if author_bio == None:#hedhi bch nchouf idha kan famma author bio DIV
        extra_P=2 # paragraph zaydin
      else:
        extra_P = 3
      if idx >= len(article_content)-extra_P:
        print(extra_P)
        break
      article_text[i]=article_text[i]+' ' +el.text
  create_new_article(title,headers,article_text)


# website_parser("https://listverse.com/2020/04/22/top-10-tv-shows-cancelled-too-soon/")