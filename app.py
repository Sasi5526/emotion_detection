
import pandas as pd
import os
from os  import getcwd
from flask import Flask, render_template, request
from fer import Video
from fer import FER
import numpy as np
import cv2


app = Flask(__name__)

directory = getcwd()


# This function structures the HTML code for displaying the table on website
def html_code_table(vid_df,table_name,file_name,side):
    table_style = '<table style="border: 2px solid; float: ' + side + '; width: 40%;">'
    table_head = '<caption style="text-align: center; caption-side: top; font-size: 140%; font-weight: bold; color:black;"><strong>' + table_name + '</strong></caption>'
    table_head_row = '<tr><th>Human Emotions</th><th>Emotion Value from the Video</th></tr>'
    
    html_code = table_style + table_head + table_head_row
    
    for i in range(len(vid_df.index)):
        row = '<tr><td>' + str(vid_df['Human Emotions'][i]) + '</td><td>' + str(vid_df['Emotion Value from the Video'][i]) + '</td></tr>'
        html_code = html_code + row
        
    html_code = html_code + '</table>'
    
    file_path = os.path.join(directory,'templates/')
    
    hs = open(file_path + file_name + '.html', 'w')
    hs.write(html_code)
    
    #print(html_code)

    
    

    

@app.route('/')
def upload():
   return render_template('upload.html')




	
@app.route('/uploaded', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      name = f.filename
      f.save('static/'+name)

   video_filename = cv2.imread('static/'+name)
   video = Video(video_filename)

# Analyze video, displaying the output
   detector = FER(mtcnn=True)
   processing_data = video.analyze(detector, display=True)

   
   def emotion_detection():


# We will now convert the analysed information into a dataframe.
# This will help us import the data as a .CSV file to perform analysis over it later
    vid_df = video.to_pandas(processing_data)
    vid_df = video.get_first_face(vid_df)
    vid_df = video.get_emotions(vid_df)


# We will now work on the dataframe to extract which emotion was prominent in the video
    angry = sum(vid_df.angry)
    disgust = sum(vid_df.disgust)
    fear = sum(vid_df.fear)
    happy = sum(vid_df.happy)
    sad = sum(vid_df.sad)
    surprise = sum(vid_df.surprise)
    neutral = sum(vid_df.neutral)

    emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
    emotions_values = [angry, disgust, fear, happy, sad, surprise, neutral]

    score_comparisons = pd.DataFrame(emotions, columns = ['Human Emotions'])
    score_comparisons['Emotion Value from the Video'] = emotions_values

    html_code_table(score_comparisons ,'Emotion detection table','emotion_detection_table','left')
    

   return render_template('output.html',filename = name)



		
if __name__ == '__main__':
   app.run(debug = False)
