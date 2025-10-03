import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

load_dotenv()

client_credentials_manager = SpotifyClientCredentials(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"), 
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

df = pd.read_csv('SpotifyFeatures.csv')
feature_cols = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence']

scaler = MinMaxScaler()
df[feature_cols] = scaler.fit_transform(df[feature_cols])

def get_song_recommendations(song_name, artist_name, num_recommendations=10):
    try:
        results = sp.search(q=f'track:{song_name} artist:{artist_name}', type='track', limit=1)
        if not results['tracks']['items']:
            return None

        track = results['tracks']['items'][0]
        track_id = track['id']

        audio_features = sp.audio_features(track_id)[0]

        input_df = pd.DataFrame([audio_features])
        input_df = input_df[feature_cols]
        input_df_scaled = scaler.transform(input_df)

        similarities = cosine_similarity(input_df_scaled, df[feature_cols])

        sim_scores = list(enumerate(similarities[0]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        top_indices = [i[0] for i in sim_scores[1:num_recommendations+1]]

        recommended_tracks = df.iloc[top_indices][['name', 'artists']]
        return recommended_tracks

    except Exception as e:
        print(f"An error occurred: {e}")
        return None