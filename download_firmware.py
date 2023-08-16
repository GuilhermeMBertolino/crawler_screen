import urllib.request
import os, sys

def parse_link(url, vendor, model):
    url.replace(" ", "%20")
    urllib.request.urlretrieve(url, f"./firmwares/{vendor}/{model}.zip")