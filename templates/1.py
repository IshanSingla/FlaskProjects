# importing modules
from lyrics_extractor import SongLyrics

# pass the GCS_API_KEY, GCS_ENGINE_ID
extract_lyrics = SongLyrics("AIzaSyAIZtzGSufntqJSf_xjU-nDMtw-I4HS93A","c711d9ef47b126b53")

ishan=extract_lyrics.get_lyrics("Tujhse Naraz Nahi Zindagi Lyrics")
print(ishan)
