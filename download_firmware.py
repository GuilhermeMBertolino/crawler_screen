import urllib.request
import os, sys

def parse_link(url, vendor, model):
    url = url.replace(" ", "%20")
    extension = url[url.rfind(".") + 1:]
    opener = urllib.request.URLopener()
    opener.addheader("User-Agent", "screen")
    opener.retrieve(url, f"./firmwares/{vendor}/{model}.{extension[:3]}")