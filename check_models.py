import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()
api_key = os.environ["GROQ_API_KEY"]

r = requests.get(
    "https://api.groq.com/openai/v1/models",
    headers={"Authorization": f"Bearer {api_key}"}
)

models = [m["id"] for m in r.json()["data"]]
print(json.dumps(models, indent=2))
