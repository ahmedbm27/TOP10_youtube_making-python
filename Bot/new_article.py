import os
#function to create new article folder
def create_new_article(article_name):
    files =['intro','conclusion','audio']

    try:
        # Create target Directory
        os.mkdir('../Articles/%s'%article_name)
        print("Directory " , article_name ,  " Created ") 
    except FileExistsError:
        print("Directory " , article_name ,  " already exists")

    for i in range (10):
        file  = open("../Articles/%s/%s.txt"%(article_name,i+1),"a+")
        file.close
        try:
        # Create target Directory
            os.mkdir('../Articles/%s/%s'%(article_name,i+1))
            print("Directory " , i+1 ,  " Created ") 
        except FileExistsError:
            print("Directory " , i+1 ,  " already exists")

    for file in files:
        text_file  = open("../Articles/%s/%s.txt"%(article_name,file),"a+")
        text_file.close
        try:
            # Create target Directory
            os.mkdir('../Articles/%s/%s'%(article_name,str(file)))
            print("Directory " , file ,  " Created ") 
        except FileExistsError:
            print("Directory " , file ,  " already exists")
create_new_article('new article')
