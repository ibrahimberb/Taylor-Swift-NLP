import pandas as pd
import lyricsgenius
import logging
import contextlib


from tqdm.auto import tqdm
from IPython.display import display
from local import get_token
from logger import get_handler

from helpers import clean_lyrics


handler = get_handler()

log = logging.getLogger(__name__)
log.handlers[:] = []
log.addHandler(handler)
log.setLevel(logging.INFO)

log.propagate = False

# disable logging from lyricsgenius
logging.getLogger("lyricsgenius").disabled = True

ALBUMS_TO_SONGS_FILEPATH = "../data/albums_to_songs.csv"
SONGS_DATAPATH = "../data/songs.csv"  # This is where we will save the data.

GENIUS_TOKEN = get_token()


class LyricsFetcher:
    def __init__(self, token: str):
        self.genius = lyricsgenius.Genius(token)
        log.info("Lyrics object initialized.")

    def get_lyrics(self, song: str, artist: str, verbose=True) -> str:
        try:
            if verbose:
                print(f"Getting lyrics for {artist} - {song}...")
            with contextlib.redirect_stdout(None):
                song = self.genius.search_song(song, artist)
            lyrics = song.lyrics
            lyrics = clean_lyrics(lyrics)
            if verbose:
                print("\033[F\033[K", end="")
            return lyrics
        except Exception as e:
            log.warning(f"Exception while getting lyrics for {artist} - {song}: {e}")
            return None


def get_albums_to_songs_data(filepath):
    data = pd.read_csv(filepath)
    log.info("Data loaded from file.")
    display(data.head())
    return data


if __name__ == "__main__":
    data = get_albums_to_songs_data(ALBUMS_TO_SONGS_FILEPATH)
    songs = data["song"].tolist()
    artist = "Taylor Swift"
    lyrics_fetcher = LyricsFetcher(GENIUS_TOKEN)

    for song in tqdm(songs, desc="Getting lyrics."):
        song_lyrics = lyrics_fetcher.get_lyrics(song, artist)
        if not song_lyrics:
            log.warning(
                f"Lyrics for {artist} - {song} not found, putting empty string."
            )

        data.loc[data["song"] == song, "lyrics"] = song_lyrics
        print(f"Processing: {song}", end="\r\r\r", flush=True)
        print("\033[F\033[K", end="", flush=True)

    data.to_csv(SONGS_DATAPATH, index=False)
    log.info("Data saved to file, enjoy!")
