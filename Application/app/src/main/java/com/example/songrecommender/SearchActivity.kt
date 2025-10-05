package com.example.songrecommender

import android.app.Activity
import android.content.Intent
import android.os.Bundle
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.textfield.TextInputEditText

class SearchActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_search)

        val etSongName = findViewById<TextInputEditText>(R.id.etSearchSongName)
        val etArtistName = findViewById<TextInputEditText>(R.id.etSearchArtistName)
        val btnSearch = findViewById<Button>(R.id.btnSearch)

        btnSearch.setOnClickListener {
            val song = etSongName.text.toString().trim()
            val artist = etArtistName.text.toString().trim()

            // Create an Intent to return the data
            val resultIntent = Intent()
            resultIntent.putExtra("SONG_NAME", song)
            resultIntent.putExtra("ARTIST_NAME", artist)
            setResult(Activity.RESULT_OK, resultIntent)

            // Close this screen and go back to the main screen
            finish()
        }
    }
}