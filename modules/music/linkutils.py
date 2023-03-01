import re
from enum import Enum
import aiohttp
from config import config

url_regex = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

session = aiohttp.ClientSession(
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'})


def clean_link(track):
    if track.startswith("https://m."):
        track = track.replace("https://m.", "https://")
    if track.startswith("http://m."):
        track = track.replace("http://m.", "https://")
    return track


def get_url(content):
    if re.search(url_regex, content):
        result = url_regex.search(content)
        url = result.group(0)
        return url
    else:
        return None


class Sites(Enum):
    YouTube = "YouTube"
    Unknown = "Unknown"


class PlaylistTypes(Enum):
    YouTube_Playlist = "YouTube Playlist"
    Unknown = "Unknown"


class Origins(Enum):
    Default = "Default"
    Playlist = "Playlist"


def identify_url(url):
    if url is None:
        return Sites.Unknown

    if "https://www.youtu" in url or "https://youtu.be" in url:
        return Sites.YouTube

    # If no match
    return Sites.Unknown


def identify_playlist(url):
    if url is None:
        return Sites.Unknown

    if "playlist?list=" in url:
        return PlaylistTypes.YouTube_Playlist

    return PlaylistTypes.Unknown
