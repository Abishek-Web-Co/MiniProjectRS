package com.example.songrecommender

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView

// The adapter now takes a function `onItemClicked` as a parameter
class SongAdapter(
    private var songs: List<Song>,
    private val onItemClicked: (Song) -> Unit
) : RecyclerView.Adapter<SongAdapter.SongViewHolder>() {

    class SongViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val songTitle: TextView = itemView.findViewById(R.id.tvSongTitle)
        val artistName: TextView = itemView.findViewById(R.id.tvArtist)

        // This function will bind the song data and set the click listener
        fun bind(song: Song, onItemClicked: (Song) -> Unit) {
            songTitle.text = song.track_name
            artistName.text = song.artist_name.replace("['", "").replace("']", "")

            // When an item in the list is clicked, call the onItemClicked function
            itemView.setOnClickListener {
                onItemClicked(song)
            }
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): SongViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_song, parent, false)
        return SongViewHolder(view)
    }

    override fun onBindViewHolder(holder: SongViewHolder, position: Int) {
        // Get the song for the current position and bind it
        val song = songs[position]
        holder.bind(song, onItemClicked)
    }

    override fun getItemCount() = songs.size

    fun updateSongs(newSongs: List<Song>) {
        songs = newSongs
        notifyDataSetChanged()
    }
}