from src.recommender import (
    Song,
    TasteTarget,
    UserProfile,
    Recommender,
    recommend_songs,
    score_song,
)

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_acousticness_score_matches_user_preference():
    song = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.5,
        "acousticness": 0.8,
    }
    preferences = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.5,
    }

    acoustic_score, acoustic_reasons = score_song(
        {**preferences, "likes_acoustic": True}, song
    )
    non_acoustic_score, _ = score_song(
        {**preferences, "likes_acoustic": False}, song
    )

    assert acoustic_score > non_acoustic_score
    assert any("acousticness fit" in reason for reason in acoustic_reasons)


def test_energy_similarity_rewards_closer_matches():
    preferences = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "likes_acoustic": False,
    }
    base_song = {
        "genre": "pop",
        "mood": "happy",
        "acousticness": 0.5,
    }
    close_score, _ = score_song(
        preferences, {**base_song, "energy": 0.8}
    )
    distant_score, _ = score_song(
        preferences, {**base_song, "energy": 0.0}
    )

    assert close_score == 4.25
    assert close_score > distant_score


def test_additional_taste_target_recommends_a_distinct_style():
    user = UserProfile(
        favorite_genre="rock",
        favorite_mood="intense",
        target_energy=0.9,
        likes_acoustic=False,
        additional_tastes=[
            TasteTarget(
                favorite_genre="lofi",
                favorite_mood="chill",
                target_energy=0.4,
                likes_acoustic=True,
            )
        ],
    )
    songs = [
        Song(1, "Intense Rock", "Artist A", "rock", "intense", 0.9, 150, 0.4, 0.6, 0.0),
        Song(2, "Chill Lofi", "Artist B", "lofi", "chill", 0.4, 80, 0.6, 0.6, 1.0),
    ]

    recommendations = Recommender(songs).recommend(user, k=2)

    assert {song.genre for song in recommendations} == {"rock", "lofi"}


def test_functional_profile_uses_best_matching_taste_target():
    profile = {
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
            }
        ],
    }
    lofi_song = {
        "title": "Chill Lofi",
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.4,
        "acousticness": 1.0,
    }

    recommendations = recommend_songs(profile, [lofi_song], k=1)

    assert recommendations[0][1] == 4.5
    assert "best fit: lofi/chill" in recommendations[0][2]


def test_main_displays_ranked_recommendation_with_scoring_reasons(monkeypatch, capsys):
    from src import main

    song = {
        "title": "Test Track",
        "genre": "rock",
        "mood": "intense",
        "energy": 0.9,
        "acousticness": 0.0,
    }
    monkeypatch.setattr(main, "load_songs", lambda _: [song])

    main.main()

    output = " ".join(capsys.readouterr().out.split())
    assert "1. Test Track" in output
    assert "Score 4.50/4.5" in output
    assert "genre match (+2.0)" in output
    assert "mood match (+1.0)" in output
    assert "energy similarity (+1.00/1.0)" in output
    assert "acousticness fit (+0.50/0.5)" in output
