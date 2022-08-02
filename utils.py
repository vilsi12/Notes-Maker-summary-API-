import os
from youtube_transcript_api import YouTubeTranscriptApi
import requests
import nlpcloud

# nlp cloud creds for text summary
NLP_CLOUD_MODEL = os.getenv('NLP_CLOUD_MODEL') 
NLP_CLOUD_TOKEN = os.getenv('NLP_CLOUD_TOKEN') 

# meaning cloud creds 
MEANING_CLOUD_API_KEY = os.getenv('MEANING_CLOUD_API_KEY')

nlp_cloud_client = nlpcloud.Client(NLP_CLOUD_MODEL,NLP_CLOUD_TOKEN)

def read_from_video(video_id):
    try:
        response_data = YouTubeTranscriptApi.get_transcript(video_id,languages=['en','en-IN'])
        full_text = ''
        for each_text in response_data:
            full_text += ' '+ each_text['text']
        print(full_text)
        return full_text
    except Exception as e:
        raise Exception(f'{e}')

def read_from_url(url):

    full_text = requests.get(url)
    return full_text.text

def read_from_document(file):
    return file.read().decode()

def get_summarized_text_nlp_cloud(text):
    response  = nlp_cloud_client.summarization(text)
    return response['summary_text']
    
def get_summarized_text_meaning_api(text):
    url = "https://api.meaningcloud.com/summarization-1.0"

    payload={
        'key': MEANING_CLOUD_API_KEY ,
        'txt': text,
        'limit': 70
    }
    return requests.post(url,data=payload).json()['summary']