# 01 Getting Started

Let's download the lyrics!

First we get the name of the songs for each album from [this](https://www.classicrockhistory.com/complete-list-of-taylor-swift-studio-albums-and-songs/) web page using the following command. 

```
python prepare_albums_to_songs.py
```

The script will prepare us `songs_to_albums.csv` file under the `data` folder by default. 

Once we have that, we can retrieve the lyrics for each song. The code is provided in the script below, and we can run it as:

```
python download_lyrics.py
```

The same process is also illustrated in `Scaper.ipynb` notebook. 

In the end, we have the the data containing the name of the song, the album and the lyrics!

| song | album | lyrics |
| --- | --- | --- | 
| Taylor Swift | Tim McGraw | He said the way my blue eyes shined ... |
| ... | ... | ... |




