package com.example.songrecommender

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.ProgressBar
import android.widget.Toast
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.textfield.TextInputEditText
import kotlinx.coroutines.launch
import android.content.Intent
import android.net.Uri

class MainActivity : AppCompatActivity() {
    private lateinit var songAdapter: SongAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val etSongName = findViewById<TextInputEditText>(R.id.etSongName)
        val etArtistName = findViewById<TextInputEditText>(R.id.etArtistName)
        val btnGetRecommendations = findViewById<Button>(R.id.btnGetRecommendations)
        val progressBar = findViewById<ProgressBar>(R.id.progressBar)
        val rvRecommendations = findViewById<RecyclerView>(R.id.rvRecommendations)

        // Setup RecyclerView and pass the click handling logic
        songAdapter = SongAdapter(emptyList()) { song ->
            // This is what happens when a song is clicked
            val spotifyUri = "spotify:track:${song.track_id}"
            val intent = Intent(Intent.ACTION_VIEW, Uri.parse(spotifyUri))

            // Add a flag to launch Spotify in a new task
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)

            // We use a try-catch block in case the user doesn't have Spotify installed
            try {
                startActivity(intent)
            } catch (e: Exception) {
                Toast.makeText(this, "Spotify app not found. Please install it.", Toast.LENGTH_SHORT).show()
            }
        }

        rvRecommendations.adapter = songAdapter
        rvRecommendations.layoutManager = LinearLayoutManager(this)

        // The button's OnClickListener remains the same
        btnGetRecommendations.setOnClickListener {
            val song = etSongName.text.toString().trim()
            val artist = etArtistName.text.toString().trim()

            if (song.isNotEmpty() && artist.isNotEmpty()) {
                progressBar.visibility = View.VISIBLE
                rvRecommendations.visibility = View.GONE

                lifecycleScope.launch {
                    try {
                        val response = RetrofitInstance.api.getRecommendations(song, artist)
                        progressBar.visibility = View.GONE
                        rvRecommendations.visibility = View.VISIBLE

                        if (response.isSuccessful && response.body() != null) {
                            songAdapter.updateSongs(response.body()!!.recommendations)
                        } else {
                            Toast.makeText(applicationContext, "Error: ${response.message()}", Toast.LENGTH_SHORT).show()
                        }
                    } catch (e: Exception) {
                        progressBar.visibility = View.GONE
                        Toast.makeText(applicationContext, "Network Error: ${e.message}", Toast.LENGTH_LONG).show()
                    }
                }
            } else {
                Toast.makeText(applicationContext, "Please enter both song and artist", Toast.LENGTH_SHORT).show()
            }
        }
    }
}