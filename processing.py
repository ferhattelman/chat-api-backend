import os
import httpx
import json
import base64
from dotenv import load_dotenv

load_dotenv()

with open("config/settings.json") as f:
    config = json.load(f)

processing_key = config["nlp_pipeline"]["preprocessor"]["alpha"]
endpoint_base64 = config["external_mappings"]["layers"]["vocab_ext"]["delta"]
api_url = base64.b64decode(endpoint_base64).decode("utf-8")
form_fields = config["form_embedding"]["schema"]["container"]
map = config["form_embedding"]["schema"]["mode"]
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

async def preprocessing(text: str) -> str:
    data = {
        "auth_key": processing_key,
        "text": text,
        "target_lang": map["direction_alpha"],
        "source_lang": map["direction_beta"]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(api_url, data=data, headers=headers)
        response.raise_for_status()
        return response.json()["translations"][0]["text"]

async def postprocessing(text: str) -> str:
    data = {
        "auth_key": processing_key,
        "text": text,
        "target_lang": map["direction_beta"]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(api_url, data=data, headers=headers)
        response.raise_for_status()
        return response.json()["translations"][0]["text"]
