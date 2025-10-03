import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Print the keys to make sure they are being read
print("--- Testing Spotify Credentials ---")
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

print(f"Loaded Client ID: {client_id}")
print(f"Loaded Client Secret: {client_secret}")
print("---------------------------------")

# Check if the keys were loaded
if not client_id or not client_secret:
    print("❌ ERROR: Client ID or Client Secret not found in .env file.")
else:
    try:
        # Attempt to authenticate
        client_credentials_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        
        # Perform a simple, harmless search query
        sp.search(q='artist:Radiohead', type='artist', limit=1)
        
        print("\n✅ SUCCESS: Authentication with Spotify was successful!")
        print("Your API keys are working correctly.")

    except Exception as e:
        print("\n❌ FAILED: Authentication with Spotify failed.")
        print("This confirms the API keys in your .env file are incorrect.")
        print(f"Error details: {e}")