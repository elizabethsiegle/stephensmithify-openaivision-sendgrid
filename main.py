# Standard library imports
import base64
import io
import os
import tempfile

# Related third-party imports
import cv2  # opencv-python-headless
import requests
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain_experimental.agents.agent_toolkits import create_csv_agent # separate langchain_experimental package
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import VideoFileClip
import openai # pip install openai==0.28
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Attachment, Disposition, FileContent, FileName, FileType, Mail)
import streamlit as st 

st.image("stephensmith.jpeg")
prompt = """
My grandma loves listening to ESPN announcer Stephen Smith. She is about to pass away from terminal cancer. Cheer both of us up by creating a short script summarizing these basketball video frames so it sounds like Stephen Smith
"""

def video_to_frames(video_file):
  # Save the uploaded video file to a temporary file
  with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmpfile:
      tmpfile.write(video_file.read())
      video_filename = tmpfile.name

  video_length = VideoFileClip(video_filename).duration

  video = cv2.VideoCapture(video_filename)
  base64Frames = []

  while video.isOpened():
    success, frame = video.read()
    if not success:
      break
    _, buffer = cv2.imencode(".jpg", frame)
    base64Frames.append(base64.b64encode(buffer).decode("utf-8"))

  video.release()
  print(len(base64Frames), "frames read.")
  return base64Frames, video_filename, video_length

def frames_to_story(base64Frames, p):
  PROMPT_MESSAGES = [
      {
          "role": "user",
          "content": [
              p,
              *map(lambda x: {"image": x, "resize": 400}, base64Frames[0::48]), #*[{"image": x, "resize": 400} for x in base64Frames[0::48]]
          ],
      },
  ]
  params = {
      "model": "gpt-4-vision-preview",
      "messages": PROMPT_MESSAGES,
      "max_tokens": 600,
  }

  result = openai.ChatCompletion.create(**params)
  print(result.choices[0].message.content)
  return result.choices[0].message.content

def text_to_audio(text):
  resp = requests.post(
    "https://api.openai.com/v1/audio/speech",
    headers={
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
    },
    json={
        "model": "tts-1",
        "input": text,
        "voice": "onyx",
    },
  )

  # Check if the request was successful
  if resp.status_code != 200:
    raise Exception("Request failed with status code")
    # ...
  # Create an in-memory bytes buffer
  audio_bytes_io = io.BytesIO()
  # Write audio data to the in-memory bytes buffer
  for chunk in resp.iter_content(chunk_size=1024 * 1024):
    audio_bytes_io.write(chunk)
    
  # Important: Seek to the start of the BytesIO buffer before returning
  audio_bytes_io.seek(0)

  # Save audio to a temporary file
  with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmpfile:
    for chunk in resp.iter_content(chunk_size=1024 * 1024):
        tmpfile.write(chunk)
    audio_filename = tmpfile.name

  return audio_filename, audio_bytes_io

def merge_audio_video(video_filename, audio_filename, output_filename):
  print("Merging audio and video...")
  print("Video filename:", video_filename)
  print("Audio filename:", audio_filename)

  # Load the video file
  video_clip = VideoFileClip(video_filename)

  # Load the audio file
  audio_clip = AudioFileClip(audio_filename)

  # Set the audio of the video clip as the audio file
  final_clip = video_clip.set_audio(audio_clip)

  # Write the result to a file (without audio)
  final_clip.write_videofile(
      output_filename, codec='libx264', audio_codec='aac')

  # Close the clips
  video_clip.close()
  audio_clip.close()

  # Return the path to the new video file
  return output_filename

st.header("Stephen Smith-ify a video :basketball:")
st.write("This [Replit](https://replit.com/) app uses [Streamlit](https://streamlit.io/), [OpenAI's new Vision API](https://platform.openai.com/docs/guides/vision), [Twilio SendGrid](https://sendgrid.com/), [LangChain CSV Agents](https://python.langchain.com/docs/integrations/toolkits/csv), and [OpenCV](https://opencv.org/) (among other libraries) to generate [Stephen Smith](https://en.wikipedia.org/wiki/Stephen_A._Smith)-esque commentary for an input basketball video file.")
uploaded_file = st.file_uploader("Upload a video file", type=["mp4"])
email = st.text_input("Email to send new video with Stephen Smith commentary to")
if st.button('Stephen Smith-ify!', type="primary") and uploaded_file is not None: 
  st.video(uploaded_file)
  with st.spinner('Processing📈...'):
      base64Frames, video_filename, video_length = video_to_frames(uploaded_file)
      rough_num_words = video_length*2 + 5

      agent = create_csv_agent(
          ChatOpenAI(temperature=1),
          "StephenCurryStats.csv", # https://www.kaggle.com/datasets/mujinjo/stephen-curry-stats-20092021-in-nba/data
          verbose=True,
          agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
      )
      stats_to_prompt = agent.run("How many games had more than 50 PTS?")

      prompt += f"(This video clip is {video_length} seconds long. Make sure the output text includes no more than {rough_num_words} words). The player scored more than 50 points in {stats_to_prompt} games"
      st.markdown(f"*prompt:  {prompt}*")
      text = frames_to_story(base64Frames, prompt)
      st.write(text)

      # Generate audio from text
      audio_filename, audio_bytes_io = text_to_audio(text)

      # Merge audio and video
      output_video_filename = os.path.splitext(video_filename)[
              0] + '_output.mp4'
      final_video_filename = merge_audio_video(video_filename, audio_filename, output_video_filename)

      # Display the result
      st.video(final_video_filename)
      message = Mail(
        from_email='stephen_smithified@replit-sendgrid-openaivision.com',
        to_emails=email,
        subject='Stephen Smith-ified Video',
        html_content='Enjoy! <3 '
      )
      with open(final_video_filename, 'rb') as f:
        data = f.read()
        f.close()
      encoded_file = base64.b64encode(data).decode()
      attachedFile = Attachment(
        FileContent(encoded_file),
        FileName('stephensmithifiedvid.mp4'),
        FileType('video/mp4'),
        Disposition('attachment')
      )
      message.attachment = attachedFile
      sg = SendGridAPIClient()
      response = sg.send(message)

      if response.status_code == 202:
        st.success("Email sent! Check your email for your video with Stephen Smith-ified commentary")
        print(f"Response Code: {response.status_code} \n Message sent!")
      else:
        st.warning("Email not sent--check email")

st.markdown(
    """
    <p style="text-align: center;font-family:Arial; color:Pink; font-size: 12px;">Made with ❤️ in SF. ✅ out <a href="https://replit.com/@LizzieSiegle/stephensmithify-openai-vision">the repl!</a></p>
    """,
    unsafe_allow_html=True, # HTML tags found in body escaped -> treated as pure text
)
