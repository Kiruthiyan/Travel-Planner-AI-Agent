import os
import requests

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in environment")

url = "https://generativelanguage.googleapis.com/v1beta/models"
headers = {"x-goog-api-key": API_KEY}
response = requests.get(url, headers=headers)
print(response.json())
