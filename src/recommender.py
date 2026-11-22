import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass, field

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class TasteTarget:
    """
    Represents one distinct set of taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


@dataclass
class UserProfile:
    """
    Represents a user's primary and additional taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    additional_tastes: List[TasteTarget] = field(default_factory=list)

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Store the catalog of songs to recommend."""
        self.songs = songs

    @staticmethod
    def _taste_targets(user: UserProfile) -> List[TasteTarget]:
        """Return the user's primary and additional taste targets."""
        return [
            TasteTarget(
                user.favorite_genre,
                user.favorite_mood,
                user.target_energy,
                user.likes_acoustic,
            ),
            *user.additional_tastes,
        ]

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs ranked by their best taste-target score."""
        if k < 0:
            raise ValueError("k must be non-negative")
        targets = self._taste_targets(user)
        return sorted(
            self.songs,
            key=lambda song: _score_song_targets(
                song.genre,
                song.mood,
                song.energy,
                song.acousticness,
                targets,
            )[0],
            reverse=True,
        )[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain how a song matches the user's best-fitting taste target."""
        score, reasons = _score_song_targets(
            song.genre,
            song.mood,
            song.energy,
            song.acousticness,
            self._taste_targets(user),
        )
        return f"Score {score:.2f}/4.5: {', '.join(reasons)}."

def load_songs(csv_path: str) -> List[Dict]:
    """Load song dictionaries with numeric attributes from a CSV file."""
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        songs = []
        for song in csv.DictReader(csv_file):
            song["id"] = int(song["id"])
            for field in ("energy", "tempo_bpm", "valence", "danceability", "acousticness"):
                song[field] = float(song[field])
            songs.append(song)
    return songs


def _score_song_features(
    genre: str,
    mood: str,
    energy: float,
    acousticness: float,
    preferred_genre: str,
    preferred_mood: str,
    target_energy: float,
    likes_acoustic: bool,
) -> Tuple[float, List[str]]:
    """Score song features against one taste target and explain the score."""
    if not 0.0 <= energy <= 1.0 or not 0.0 <= target_energy <= 1.0:
        raise ValueError("energy and target_energy must be between 0.0 and 1.0")
    if not 0.0 <= acousticness <= 1.0:
        raise ValueError("acousticness must be between 0.0 and 1.0")
    if not isinstance(likes_acoustic, bool):
        raise ValueError("likes_acoustic must be a boolean")

    genre_match = genre == preferred_genre
    mood_match = mood == preferred_mood
    genre_points = 1.0 if genre_match else 0.0
    mood_points = 1.0 if mood_match else 0.0
    energy_points = 2.0 * (1.0 - abs(energy - target_energy))
    acousticness_fit = acousticness if likes_acoustic else 1.0 - acousticness
    acousticness_points = 0.5 * acousticness_fit

    reasons = [
        "genre match (+1.0)" if genre_match else "genre differs (+0.0)",
        "mood match (+1.0)" if mood_match else "mood differs (+0.0)",
        f"energy similarity (+{energy_points:.2f}/2.0)",
        f"acousticness fit (+{acousticness_points:.2f}/0.5)",
    ]
    return genre_points + mood_points + energy_points + acousticness_points, reasons


def _score_song_targets(
    genre: str,
    mood: str,
    energy: float,
    acousticness: float,
    taste_targets: List[TasteTarget],
) -> Tuple[float, List[str]]:
    """Return the highest song score and reasons across taste targets."""
    if not taste_targets:
        raise ValueError("A user profile must contain at least one taste target")

    scored_targets = [
        (
            *_score_song_features(
                genre,
                mood,
                energy,
                acousticness,
                target.favorite_genre,
                target.favorite_mood,
                target.target_energy,
                target.likes_acoustic,
            ),
            target,
        )
        for target in taste_targets
    ]
    score, reasons, best_target = max(scored_targets, key=lambda result: result[0])
    return score, [
        f"best fit: {best_target.favorite_genre}/{best_target.favorite_mood}",
        *reasons,
    ]


def _taste_target_from_dict(preferences: Dict) -> TasteTarget:
    """Create a taste target from a dictionary of preferences."""
    if not isinstance(preferences, dict):
        raise ValueError("Each taste target must be a dictionary")
    required_preferences = (
        "favorite_genre",
        "favorite_mood",
        "target_energy",
        "likes_acoustic",
    )
    missing = [key for key in required_preferences if key not in preferences]
    if missing:
        raise ValueError(f"Missing taste-target values: {', '.join(missing)}")
    return TasteTarget(
        favorite_genre=preferences["favorite_genre"],
        favorite_mood=preferences["favorite_mood"],
        target_energy=preferences["target_energy"],
        likes_acoustic=preferences["likes_acoustic"],
    )


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against user preferences and return the score and reasons."""
    primary_target = _taste_target_from_dict(user_prefs)
    additional_preferences = user_prefs.get("additional_tastes", [])
    if not isinstance(additional_preferences, list):
        raise ValueError("additional_tastes must be a list of taste-target dictionaries")
    targets = [
        primary_target,
        *(_taste_target_from_dict(target) for target in additional_preferences),
    ]
    return _score_song_targets(
        song["genre"],
        song["mood"],
        song["energy"],
        song["acousticness"],
        targets,
    )

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return the top k songs with scores and explanations."""
    if k < 0:
        raise ValueError("k must be non-negative")

    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = f"Score {score:.2f}/4.5: {', '.join(reasons)}."
        scored_songs.append((song, score, explanation))
    return sorted(scored_songs, key=lambda recommendation: recommendation[1], reverse=True)[:k]
