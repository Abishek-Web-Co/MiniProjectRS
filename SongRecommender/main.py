from fastapi import FastAPI, HTTPException
from recommender import get_song_recommendations
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# This is needed to allow your app to talk to the server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/recommend")
def recommend_endpoint(song: str, artist: str):
    if not song or not artist:
        raise HTTPException(status_code=400, detail="Song and artist parameters are required.")

    recommendations_df = get_song_recommendations(song, artist)

    if recommendations_df is None:
        raise HTTPException(status_code=404, detail="Song not found or an error occurred.")

    return {"recommendations": recommendations_df.to_dict(orient="records")}