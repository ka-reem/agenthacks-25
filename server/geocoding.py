import googlemaps
from datetime import datetime
import os
import requests
import base64

gmaps = googlemaps.Client(key=os.environ["GOOGLE_API_KEY"])


def geocode(address: str):
    return gmaps.geocode(address)


def street_view(lat, lon):
    url = f"https://maps.googleapis.com/maps/api/streetview?size=700x400&location={lat},{lon}&key={os.environ['GOOGLE_API_KEY']}"
    img = requests.get(url)
    return base64.b64encode(img.content).decode("utf-8")
