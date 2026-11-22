"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from textwrap import fill

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 
    print(f"Loaded songs: {len(songs)}")

    taste_profile = {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.9,
        "likes_acoustic": False,
        "additional_tastes": [
            {
                "favorite_genre": "lofi",
                "favorite_mood": "chill",
                "target_energy": 0.4,
                "likes_acoustic": True,
            },
        ],
    }

    recommendations = recommend_songs(taste_profile, songs, k=5)

    print("\nTop recommendations:\n")
    for rank, (song, _, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']}")
        print(fill(explanation, width=80, initial_indent="   ", subsequent_indent="   "))
        print()


if __name__ == "__main__":
    main()
