![header image](https://github.com/elizabethsiegle/stephensmithify-openaivision-sendgrid/assets/8932430/767d8558-1942-4716-8a88-a44c524d7b4a)

### Generate NBA Commentary in the style of someone with Stephen Smith-like qualities using
- [Twilio SendGrid](https://www.twilio.com/en-us/sendgrid/email-api)
- [OpenAI GPT-4V API](https://platform.openai.com/docs/guides/vision) (and OpenAI TTS)
- [Replit](https://replit.com/)
- [LangChain](https://langchain.com/)
- [OpenCV](https://opencv.org/)

You can [test out the app on Replit here](https://stephensmithify-openaivision-sendgrid-lizziesiegle.replit.app/) or [play with the code on Replit here](https://replit.com/@LizzieSiegle/stephensmithify-openai-vision)

Thank you to [my coworker and AccelerateSF teammate Chris Brox](https://ckbrox.com/) for helping with the [YouTube video](https://www.youtube.com/watch?v=4fyQE5SCpTY)!


#### Prereqs
- Twilio SendGrid account - [make an account here](https://signup.sendgrid.com/) and [make an API key here](https://app.sendgrid.com/settings/api_keys)
- An email address to test out this project
- A Replit account for hosting the application – [make an account here](https://replit.com/signup)
- OpenAI account - [make an account here](https://platform.openai.com/signup?launch) and [find your API key here](https://platform.openai.com/account/api-keys)

You'll add your secret keys to Replit as such
![New Secret](https://github.com/elizabethsiegle/stephensmithify-openaivision-sendgrid/assets/8932430/ee5cacfe-21a9-4292-b698-7dcc4cf784c8)

![Replit secret keys](https://github.com/elizabethsiegle/stephensmithify-openaivision-sendgrid/assets/8932430/d0e640a1-42ba-4ccc-affb-67a7d40de0d2)


Dependencies:
- `moviepy` to help process video and audio
- `cv2` (OpenCV) to help handle video frames
- `langchain` to read and parse a CSV for relevant statistics
- `openai` for OpenAI's GPT-4V and text-to-speech (TTS) APIs
- `requests` for making HTTP requests to OpenAI's API
- `streamlit` to create a web-based UI in Python
- `tempfile` to help handle temporary files while processing

These are added to Replit by clicking on _packages_:

![Replit packages](https://github.com/elizabethsiegle/stephensmithify-openaivision-sendgrid/assets/8932430/75231199-abe5-4e76-81e2-bbd2c0176603)
