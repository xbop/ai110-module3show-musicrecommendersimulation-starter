# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world platforms often combine a person's listening behavior, item attributes, similar users' preferences, and contextual signals. This simulation uses a simpler content-based approach:

1. **Input:** Load song attributes from `data/songs.csv` and read the user's taste profile, which can include multiple distinct taste targets.
2. **Score each song against each target:** Add **2.0** for an exact genre match and **1.0** for an exact mood match. Add up to **1.0** for energy similarity, calculated as `1 - abs(song energy - target energy)`. Add up to **0.5** for acousticness fit: `acousticness` when the user likes acoustic music, or `1 - acousticness` otherwise.
3. **Choose and rank:** Keep each song's highest score across the user's taste targets, sort songs by that score in descending order, and return the top `k` with an explanation.

The maximum score per target is **4.5**. This simulation does not use listener histories or collaborative filtering.

The simulation's data objects use these features:

- **`Song`**: `id`, `title`, and `artist` identify the track; `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness` describe it.
- **`UserProfile`**: a primary `favorite_genre`, `favorite_mood`, `target_energy`, and `likes_acoustic` preference, with optional additional taste targets for distinct styles.

The CLI profile includes two taste targets—rock/intense/high-energy and lofi/chill/lower-energy—with their own acousticness preferences.

**Potential biases and limitations:** Genre receives twice the points of mood, so a genre match can outweigh a mood match; exact category matching also misses related genres or moods. Choosing the best of multiple taste targets can favor one style without ensuring variety. Recommendations are further limited by the small, hand-selected catalog and simplified audio features.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output for the default rock/intense and lofi/chill taste targets:

```text
Loaded songs: 18

Top recommendations:

1. Storm Runner
   Score 4.44/4.5: best fit: rock/intense, genre match (+2.0), mood match
   (+1.0), energy similarity (+0.99/1.0), acousticness fit (+0.45/0.5).

2. Library Rain
   Score 4.38/4.5: best fit: lofi/chill, genre match (+2.0), mood match (+1.0),
   energy similarity (+0.95/1.0), acousticness fit (+0.43/0.5).

3. Midnight Coding
   Score 4.33/4.5: best fit: lofi/chill, genre match (+2.0), mood match (+1.0),
   energy similarity (+0.98/1.0), acousticness fit (+0.35/0.5).

4. Focus Flow
   Score 3.39/4.5: best fit: lofi/chill, genre match (+2.0), mood differs
   (+0.0), energy similarity (+1.00/1.0), acousticness fit (+0.39/0.5).

5. Gym Hero
   Score 2.44/4.5: best fit: rock/intense, genre differs (+0.0), mood match
   (+1.0), energy similarity (+0.97/1.0), acousticness fit (+0.47/0.5).
```

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



