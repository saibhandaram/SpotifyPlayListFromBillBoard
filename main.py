import export as export
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from pprint import pprint

#https://developer.spotify.com/dashboard/
#https://spotipy.readthedocs.io/en/2.22.1/
CLIENT_ID = ""
CLIENT_SECRET = ""
USER_NAME = ""

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username=USER_NAME,
    )
)
user_id = sp.current_user()["id"]
#print(user_id)

date = input("Enter Date YYYY-MM-DD Format:")

url = f"https://www.billboard.com/charts/hot-100/{date}/"
# print(url)
response = requests.get(url)

html_doc = response.text
soup = BeautifulSoup(html_doc, 'html.parser')
# print(soup.prettify())

all_titles = soup.find_all("h3", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 "
                                        "lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 "
                                        "u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 "
                                        "u-max-width-230@tablet-only")

song_uris = []
year = date.split("-")[0]

# playlist_name = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False, collaborative=False,
#                                         description='BillBoard on a Day')
# pprint(playlist_name)

playlist_info = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
#pprint(playlist_info["id"])

for title in all_titles:
    my_song = title.getText().strip()
    result = sp.search(q=f"track:{my_song} year:{year}", type="track")

    # pprint(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
        # pprint(song_uris)
    except IndexError:
        print(f"{my_song} doesn't exist in Spotify. Skipped.")

sp.playlist_add_items(playlist_id=playlist_info["id"], items=song_uris, position=None)
