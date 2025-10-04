import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# --- Step 1: Load Environment Variables ---
load_dotenv()

# --- Step 2: Initialize FastAPI App ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Step 3: Global Variables ---
sp = None
df = None
scaler = None

# --- Step 4: Startup Event ---
@app.on_event("startup")
def startup_event():
    global sp, df, scaler

    # Authenticate with Spotify (for search)
    try:
        client_credentials_manager = SpotifyClientCredentials(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
        )
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        print("✅ Spotify authentication successful.")
    except Exception as e:
        print(f"❌ CRITICAL ERROR: Could not authenticate with Spotify. Error: {e}")
        return

    # Load and prepare dataset
    try:
        df = pd.read_csv('SpotifyFeatures.csv')

        # Feature columns for similarity
        feature_cols = ['acousticness', 'danceability', 'energy', 'instrumentalness',
                        'liveness', 'loudness', 'speechiness', 'tempo', 'valence']

        # Normalize features
        scaler = MinMaxScaler()
        df[feature_cols] = scaler.fit_transform(df[feature_cols])

        print("✅ Dataset loaded and prepared successfully.")
    except FileNotFoundError:
        print("❌ CRITICAL ERROR: SpotifyFeatures.csv not found.")
        df = None


# --- Step 5: Recommendation Logic ---
def find_recommendations(song_name, artist_name, num_recommendations=10):
    global sp, df, scaler

    if sp is None or df is None:
        return None

    try:
        feature_cols = ['acousticness', 'danceability', 'energy', 'instrumentalness',
                        'liveness', 'loudness', 'speechiness', 'tempo', 'valence']

        # Step 1: Search song in Spotify to confirm existence
        results = sp.search(q=f'track:{song_name} artist:{artist_name}', type='track', limit=1)
        if not results['tracks']['items']:
            print(f"❌ Song '{song_name}' by '{artist_name}' not found on Spotify.")
            return None

        track = results['tracks']['items'][0]
        track_name = track['name']
        track_artist = track['artists'][0]['name']

        # Step 2: Find matching song in local CSV
        song_row = df[(df['track_name'].str.lower() == track_name.lower()) &
                      (df['artist_name'].str.lower().str.contains(track_artist.lower()))]

        if song_row.empty:
            print(f"❌ Song '{track_name}' by '{track_artist}' not found in dataset.")
            return None

        # Step 3: Prepare input for similarity
        input_df = song_row[feature_cols]
        input_df_scaled = scaler.transform(input_df)

        # Step 4: Calculate similarity
        similarities = cosine_similarity(input_df_scaled, df[feature_cols])
        sim_scores = list(enumerate(similarities[0]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        top_indices = [i[0] for i in sim_scores[1:num_recommendations + 1]]

        # Step 5: Return recommendations
        return df.iloc[top_indices][['track_name', 'artist_name']]

    except Exception as e:
        print(f"An error occurred during recommendation: {e}")
        return None


# --- Step 6: API Endpoint ---
@app.get("/recommend")
def recommend_endpoint(song: str, artist: str):
    if not song or not artist:
        raise HTTPException(status_code=400, detail="Song and artist parameters are required.")

    recommendations_df = find_recommendations(song, artist)

    if recommendations_df is None or recommendations_df.empty:
        raise HTTPException(status_code=404, detail="Song not found or an error occurred.")

    return {"recommendations": recommendations_df.to_dict(orient="records")}
