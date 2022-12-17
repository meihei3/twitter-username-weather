import json
import requests
import os
import re
from requests_oauthlib import OAuth1

WEATHER_URL = "http://api.openweathermap.org/data/2.5/forecast"
TWITTER_SHOW_URL = "https://api.twitter.com/1.1/users/show.json"
TWITTER_UPDATE_URL = "https://api.twitter.com/1.1/account/update_profile.json"
PARAMS = {
    "q": "Tokyo,jp",
    "APPID": os.environ.get("OPEN_WEATHER_MAP_API_KEY")
}
EMOJI = {
    "Thunderstorm": "⚡",
    "Drizzle": "🌨",
    "Rain": "☔",
    "Snow": "⛄",
    "Clear_day": "☀",
    "Clear_night": "🌙",
    "Clouds": "☁",
    "Fog": "🌫"
}
CK = os.environ.get("TWITTER_CK")
CS = os.environ.get("TWITTER_CS")
AT = os.environ.get("TWITTER_AT")
AS = os.environ.get("TWITTER_AS")

AUTH = OAuth1(CK, CS, AT, AS)


def get_emoji(wh: str, icon: str = "d") -> str:
    if wh in EMOJI:
        return EMOJI[wh]
    if wh == "Clear":
        if icon[-1] == "d":
            return EMOJI["Clear_day"]
        return EMOJI["Clear_night"]
    return EMOJI["Fog"]


def get_weather():
    res = requests.get(WEATHER_URL, params=PARAMS)
    _json = json.loads(res.text)
    content = _json["list"][1]["weather"][0]
    content["emoji"] = get_emoji(content["main"], icon=content["icon"])
    return content


def get_user_name(_id: str = "1302858168") -> str:
    return json.loads(
        requests.get(TWITTER_SHOW_URL, params={"user_id": _id}, auth=AUTH).text
    )["name"]


def update_name(_name: str):
    requests.post(TWITTER_UPDATE_URL, data={"name": _name}, auth=AUTH)


def lambda_handler(event, context):
    w = get_weather()
    name = get_user_name()
    if name[-1] in EMOJI.values():
        name = name[:-1]
    update_name(name+w["emoji"])
    return w


if __name__ == '__main__':
    w = get_weather()
    print(w)
