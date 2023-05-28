"""
TODO: For now, this script is only used to get the list of songs from the
        website. In the future, I may try to get the name of the songs 
        along with album names via API calls.
"""

import logging

import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from IPython.display import display

from logger import get_handler
from helpers import clean_song_title

handler = get_handler()

log = logging.getLogger(__name__)
log.handlers[:] = []
log.addHandler(handler)
log.setLevel(logging.INFO)

SONG_SCRAPE_URL = "https://www.classicrockhistory.com/complete-list-of-taylor-swift-studio-albums-and-songs/"

ALBUM_TO_SONGS_FILEPATH = (
    "../data/albums_to_songs.csv"  # This is where we will save the data.
)


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def get_content(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        log.info("Request successful")
        return response.content
    else:
        log.error("Request failed with status code:", response.status_code)
        raise Exception("Request failed with status code:", response.status_code)


def get_album_to_songs(content):
    album_to_songs = defaultdict(list)
    soup = BeautifulSoup(content, "html.parser")

    p_elements = soup.find_all("p")
    h3_elements = soup.find_all("h2")
    combined_elements = p_elements + h3_elements
    sorted_elements = sorted(combined_elements, key=lambda element: element.sourceline)

    current_album = None
    for element in sorted_elements:
        if not element.text.strip():
            continue

        if element.name == "h2":
            log.debug("=====================================")
            log.debug(element.text)
            current_album = element.text
            log.debug("=====================================")

        if re.match(r"^\d+\.", element.text):
            songs = element.text.split("\n")
            for song in songs:
                song_name = clean_song_title(song)
                log.debug(song_name)
                album_to_songs[current_album].append(song_name)

    log.info(f"Found {len(album_to_songs)} albums.")
    return album_to_songs


def save_albums_to_songs(albums_to_songs, filename):
    data = pd.DataFrame(
        [(album, song) for album, songs in albums_to_songs.items() for song in songs],
        columns=["album", "song"],
    )

    data.to_csv(filename, index=False)
    display(data.head())
    log.info(f"Saved {filename} to disk.")


if __name__ == "__main__":
    response = get_content(SONG_SCRAPE_URL)
    albums_to_songs = get_album_to_songs(response)
    save_albums_to_songs(albums_to_songs, filename=ALBUM_TO_SONGS_FILEPATH)
    log.info("Ta da!")
