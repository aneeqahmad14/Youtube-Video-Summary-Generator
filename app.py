import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()  # Load all the enviroment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""Role: As a YouTube video summarizer, your responsibility is to distill the essence of the provided transcript into a concise summary.

Steps:

Content Analysis:

Begin by thoroughly analyzing the transcript to understand the main message, key themes, and supporting details.
Core Insights Identification:

Identify the most important insights, arguments, and takeaways that are central to the video's content. Focus on capturing the essence of the video rather than peripheral details.
Summary Creation:

Structure your summary in bullet points for clarity, emphasizing the key points in a logical order.
Ensure the summary is informative yet succinct, covering all critical information while remaining within a 250-word limit.
Quality Check:

Review the summary to ensure it accurately reflects the content and intent of the video. The summary should be clear, coherent, and easy to understand.
Instructions: Provide the summarized content based on the transcript provided below:

Note: Make a points that are nessaccary according to the video transcript """

## Getting the transcript form yt videos

def extract_transcript(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id,)
        
        transcript =""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript
    except Exception as e:
        raise e

## Getting the summary
def generate_content(transcript_text,prompt):

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+transcript_text)
    return response.text


st.title("Youtube Video Summary Generator")
youtube_video_link = st.text_input("Enter YouTube Video Link:")

if youtube_video_link:
    video_id = youtube_video_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)


if st.button("Generate Summary"):
    transcript_text=extract_transcript(youtube_video_link)

    if transcript_text:
        summary  = generate_content(transcript_text, prompt)
        st.markdown("## Detailed Summary")
        st.write(summary)





