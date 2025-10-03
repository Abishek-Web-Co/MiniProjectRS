import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

def get_song_recommendations(song_name, artist_name, num_recommendations=10):
    """
    Finds a song on Spotify and returns a list of recommended tracks
    based on audio features and cosine similarity.
    """
    # --- Step 1: Setup and Authentication ---
    
    # Load environment variables from .env file (for SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET)
    load_dotenv()

    # Authenticate with Spotify using the Client Credentials Flow
    try:
        client_credentials_manager = SpotifyClientCredentials(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
        )
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    except Exception as e:
        print(f"Authentication Error: {e}")
        return None

    # --- Step 2: Data Loading and Preparation ---

    # Load the dataset of Spotify tracks
    df = pd.read_csv('SpotifyFeatures.csv')

    # Define the audio features to be used for comparison
    feature_cols = ['acousticness', 'danceability', 'energy', 'instrumentalness',
                    'liveness', 'loudness', 'speechiness', 'tempo', 'valence']

    # Scale the features to ensure they are all weighted equally
    scaler = MinMaxScaler()
    df[feature_cols] = scaler.fit_transform(df[feature_cols])

    # --- Step 3: Find Input Song and its Features ---

    try:
        # Search for the user's input song
        results = sp.search(q=f'track:{song_name} artist:{artist_name}', type='track', limit=1)
        
        # Check if the song was found
        if not results['tracks']['items']:
            print(f"Song '{song_name}' by '{artist_name}' not found.")
            return None  # Return None if the song is not found

        track = results['tracks']['items'][0]
        track_id = track['id']

        # Get the audio features for the input song
        audio_features = sp.audio_features(track_id)[0]

    except Exception as e:
        print(f"Error searching for song or getting features: {e}")
        return None

    # --- Step 4: Calculate Similarity and Get Recommendations ---

    # Create a DataFrame for the input song's features
    input_df = pd.DataFrame([audio_features])
    input_df = input_df[feature_cols]

    # Scale the input song's features using the same scaler
    input_df_scaled = scaler.transform(input_df)

    # Calculate the cosine similarity between the input song and all songs in the dataset
    similarities = cosine_similarity(input_df_scaled, df[feature_cols])

    # Get the similarity scores and sort them in descending order
    sim_scores = list(enumerate(similarities[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices of the top N most similar songs (excluding the song itself)
    top_indices = [i[0] for i in sim_scores[1:num_recommendations + 1]]

    # Retrieve the recommended tracks from the original DataFrame
    recommended_tracks = df.iloc[top_indices][['name', 'artists']]

    return recommended_tracks