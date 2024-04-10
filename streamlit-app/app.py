import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import os

load_dotenv() 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# prompt="""You are Yotube video summarizer. You will be taking the transcript text
# and summarizing the entire video and providing the important summary in points
# within 250 words. Mention keywords separately in a comma separated format. Please provide 
# the summary of the text given here:  """

prompt = """
You are Yotube video summarizer. You will be given the transcript text of a YouTube video. 
You are supposed to summarize the entire video in points (either numbered or bulleted) and optionally subpoints within 250 words. 
Please summarize the transcript here: 
"""

def get_youtube_video_id(url):
    return url.split('=')[1]

## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=get_youtube_video_id(youtube_video_url)
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e
    
## getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text,prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

st.title("YouTube AI Summarizer")
youtube_link = st.text_input("Enter YouTube Video Link:")

if st.button("Get Summary"):
    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.write(summary)
