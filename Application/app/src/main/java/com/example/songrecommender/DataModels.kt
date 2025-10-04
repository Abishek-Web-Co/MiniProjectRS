package com.example.songrecommender

// NOTE: The variable names here MUST EXACTLY MATCH the keys in the JSON from your Python server.
// The JSON from your latest backend has "track_name" and "artist_name".
data class Song(
    val track_name: String,
    val artist_name: String
)

data class RecommendationResponse(
    val recommendations: List<Song>
)