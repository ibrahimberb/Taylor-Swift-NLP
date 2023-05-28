import re


def clean_song_title(song_title: str):
    song_name = re.sub(r"^\d+\.", "", song_title).strip()
    if "Come Back" in song_title:
        song_name = re.sub(r"^\d+\.", "", song_name).strip()
    song_name = re.sub(r"\u2018|\u2019", "'", song_name)
    song_name = re.sub(r"\u201C|\u201D", '"', song_name)
    song_name = _clean(song_name)
    song_name = song_name.replace('"', "")

    return song_name


def clean_lyrics(lyrics: str) -> str:
    # Remove first line (title + verse line)
    lyrics = lyrics.split(sep="\n", maxsplit=1)[1]
    # Replace special quotes with normal quotes
    lyrics = re.sub(r"\u2018|\u2019", "'", lyrics)
    lyrics = re.sub(r"\u201C|\u201D", '"', lyrics)
    lyrics = _clean(lyrics)
    return lyrics


def _clean(text: str) -> str:
    # Replace special unicode spaces with standard space
    text = re.sub(
        r"[\u00A0\u1680​\u180e\u2000-\u2009\u200a​\u200b​\u202f\u205f​\u3000]",
        " ",
        text,
    )
    # Replace dashes with space and single hyphen
    text = re.sub(r"\u2013|\u2014", " - ", text)
    # Replace hyperlink text
    text = re.sub(r"[0-9]*URLCopyEmbedCopy", "", text)
    text = re.sub(r"[0-9]*Embed", "", text)
    text = re.sub(r"[0-9]*EmbedShare", "", text)

    ticket_pattern = r"See .* as low as \$.+You might also like"
    text = re.sub(ticket_pattern, "", text)

    return text
