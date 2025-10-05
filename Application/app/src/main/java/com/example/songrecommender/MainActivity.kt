package com.example.songrecommender

import android.app.Activity
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.view.View
import android.widget.ProgressBar
import android.widget.TextView
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {

    private lateinit var songAdapter: SongAdapter

    // This is the new way to handle getting a result from another activity
    private val searchActivityResultLauncher = registerForActivityResult(
        ActivityResultContracts.StartActivityForResult()
    ) { result ->
        if (result.resultCode == Activity.RESULT_OK) {
            val data = result.data
            val songName = data?.getStringExtra("SONG_NAME")
            val artistName = data?.getStringExtra("ARTIST_NAME")

            if (!songName.isNullOrEmpty() && !artistName.isNullOrEmpty()) {
                // When we get a result, fetch recommendations for the new song
                val progressBar = findViewById<ProgressBar>(R.id.progressBar)
                val rvRecommendations = findViewById<RecyclerView>(R.id.rvRecommendations)
                fetchRecommendations(songName, artistName, progressBar, rvRecommendations)
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val tvSearch = findViewById<TextView>(R.id.tvSearch)
        val progressBar = findViewById<ProgressBar>(R.id.progressBar)
        val rvRecommendations = findViewById<RecyclerView>(R.id.rvRecommendations)

        setupRecyclerView(rvRecommendations)

        // Load default recommendations on startup
        fetchRecommendations("Blinding Lights", "The Weeknd", progressBar, rvRecommendations)

        // Make the search bar clickable
        tvSearch.setOnClickListener {
            val intent = Intent(this, SearchActivity::class.java)
            searchActivityResultLauncher.launch(intent)
        }
    }

    // The rest of the functions are the same as before
    private fun setupRecyclerView(rvRecommendations: RecyclerView) {
        songAdapter = SongAdapter(emptyList()) { song ->
            val spotifyUri = "spotify:track:${song.track_id}"
            val intent = Intent(Intent.ACTION_VIEW, Uri.parse(spotifyUri))
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            try {
                startActivity(intent)
            } catch (e: Exception) {
                Toast.makeText(this, "Spotify app not found.", Toast.LENGTH_SHORT).show()
            }
        }
        rvRecommendations.adapter = songAdapter
        rvRecommendations.layoutManager = LinearLayoutManager(this)
    }

    private fun fetchRecommendations(song: String, artist: String, progressBar: ProgressBar, rvRecommendations: RecyclerView) {
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
    }
}