import os
import pandas as pd
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import seaborn as sns

# load the .env file variables
load_dotenv()

ARTISTID = "7dGJo4pcD2V6oG8kP0tJRR"

client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('SECRET_ID')

con = spotipy.Spotify(auth_manager = SpotifyClientCredentials(client_id = client_id,client_secret = client_secret))

response = con.artist_top_tracks(ARTISTID)
if response:
  # We keep the "tracks" object of the answer
    tracks = response["tracks"]
  # We select, for each song, the data we are interested in and discard the rest
    tracks = [{k: (v/(1000*60))%60 if k == "duration_ms" else v for k, v in track.items() if k in ["name", "popularity", "duration_ms"]} for track in tracks]

tracks_df = pd.DataFrame.from_records(tracks)
tracks_df.sort_values(["popularity"], inplace = True)

print(tracks_df.head(3))    

scatter_plot = sns.scatterplot(data = tracks_df, x = "popularity", y = "duration_ms")
fig = scatter_plot.get_figure()
fig.savefig("scatter_plot.png")