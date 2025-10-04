package com.example.songrecommender

import retrofit2.Response
import retrofit2.http.GET
import retrofit2.http.Query

interface ApiService {
    @GET("recommend")
    suspend fun getRecommendations(
        @Query("song") song: String,
        @Query("artist") artist: String
    ): Response<RecommendationResponse>
}