import os
import json
from time import sleep
import requests
import dotenv

dotenv.load_dotenv()
clientid = os.getenv("CLIENTID")
token = os.getenv("TOKEN")
broadcasterid = os.getenv("BROADCASTERID")
webhookurl = os.getenv("WEBHOOKURL")


def create_clip():
    web_request = requests.post(
        "https://api.twitch.tv/helix/clips?broadcaster_id=" + broadcasterid,
        headers={"Authorization": "Bearer " + token, "Client-ID": clientid},
    )
    sleep(5)
    return json.loads(web_request.text).get("data")[0].get("id")


def get_clip(clip_id):
    clip_id = str(clip_id)
    web_request = requests.get(
        "https://api.twitch.tv/helix/clips?id=" + clip_id,
        headers={"Authorization": "Bearer " + token, "Client-ID": clientid},
    )
    return json.loads(web_request.text)


def create_embed(clip_id):
    clip = get_clip(clip_id)
    imageurl = str(clip.get("data")[0].get("thumbnail_url"))
    cliptimestamp = str(clip.get("data")[0].get("created_at"))
    clipurl = str(clip.get("data")[0].get("url"))
    cliptitle = str(clip.get("data")[0].get("title"))
    web_request = requests.post(
        webhookurl,
        data=json.dumps(
            {
                "content": "",
                "embeds": [
                    {
                        "title": cliptitle,
                        "description": clipurl,
                        "url": clipurl,
                        "timestamp": cliptimestamp,
                        "color": 0xFF0000,
                        "image": {"url": imageurl},
                    }
                ],
            }
        ),
        headers={"Content-Type": "application/json"},
    )
    return web_request.text


clip_id = str(create_clip())
print(create_embed(clip_id))
