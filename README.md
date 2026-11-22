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
2. **Score each song against each target:** Add **1.0** for an exact genre match and **1.0** for an exact mood match. Add up to **2.0** for energy similarity, calculated as `2 * (1 - abs(song energy - target energy))`. Add up to **0.5** for acousticness fit: half of `acousticness` when the user likes acoustic music, or half of `1 - acousticness` otherwise.
3. **Choose and rank:** Keep each song's highest score across the user's taste targets, sort songs by that score in descending order, and return the top `k` with an explanation.

The maximum score per target is **4.5**. This simulation does not use listener histories or collaborative filtering.

The simulation's data objects use these features:

- **`Song`**: `id`, `title`, and `artist` identify the track; `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness` describe it.
- **`UserProfile`**: a primary `favorite_genre`, `favorite_mood`, `target_energy`, and `likes_acoustic` preference, with optional additional taste targets for distinct styles.

The CLI defines High-Energy Pop, Chill Lofi, and Deep Intense Rock profiles. Its default combines the rock/intense and lofi/chill targets, each with its own acousticness preference.

**Potential biases and limitations:** Energy similarity can outweigh a genre or mood match; exact category matching also misses related genres or moods. Choosing the best of multiple taste targets can favor one style without ensuring variety. Recommendations are further limited by the small, hand-selected catalog and simplified audio features.

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
   Score 4.43/4.5: best fit: rock/intense, genre match (+1.0), mood match
   (+1.0), energy similarity (+1.98/2.0), acousticness fit (+0.45/0.5).

2. Library Rain
   Score 4.33/4.5: best fit: lofi/chill, genre match (+1.0), mood match (+1.0),
   energy similarity (+1.90/2.0), acousticness fit (+0.43/0.5).

3. Midnight Coding
   Score 4.31/4.5: best fit: lofi/chill, genre match (+1.0), mood match (+1.0),
   energy similarity (+1.96/2.0), acousticness fit (+0.35/0.5).

4. Gym Hero
   Score 3.42/4.5: best fit: rock/intense, genre differs (+0.0), mood match
   (+1.0), energy similarity (+1.94/2.0), acousticness fit (+0.47/0.5).

5. Focus Flow
   Score 3.39/4.5: best fit: lofi/chill, genre match (+1.0), mood differs
   (+0.0), energy similarity (+2.00/2.0), acousticness fit (+0.39/0.5).
```

---

## Experiments You Tried

**Weight shift:** The current experiment halves the genre match weight from 2 to 1 and doubles the energy weight from 1 to 2. For the default profile, Gym Hero moved from fifth to fourth, ahead of Focus Flow; the first three songs stayed in the same order.

The following baseline experiments used deliberately conflicting or unavailable preferences before the weight shift (genre up to 2 points and energy up to 1). Each profile was scored against the catalog and its top five results are shown below.

### High-energy sad pop

The catalog has no `sad` mood, so happy or intense pop songs lead despite the requested mood; genre still earns two points.

```text
High-energy sad pop
Profile: {'favorite_genre': 'pop', 'favorite_mood': 'sad', 'target_energy': 0.9, 'likes_acoustic': True}
Top 5 recommendations:
1. Sunrise City
   Score 3.01/4.5: best fit: pop/sad, genre match (+2.0), mood differs (+0.0),
   energy similarity (+0.92/1.0), acousticness fit (+0.09/0.5).
2. Gym Hero
   Score 2.99/4.5: best fit: pop/sad, genre match (+2.0), mood differs (+0.0),
   energy similarity (+0.97/1.0), acousticness fit (+0.03/0.5).
3. Carnival Steps
   Score 1.06/4.5: best fit: pop/sad, genre differs (+0.0), mood differs (+0.0),
   energy similarity (+0.98/1.0), acousticness fit (+0.09/0.5).
4. Storm Runner
   Score 1.04/4.5: best fit: pop/sad, genre differs (+0.0), mood differs (+0.0),
   energy similarity (+0.99/1.0), acousticness fit (+0.05/0.5).
5. Rooftop Lights
   Score 1.03/4.5: best fit: pop/sad, genre differs (+0.0), mood differs (+0.0),
   energy similarity (+0.86/1.0), acousticness fit (+0.17/0.5).
```

### Intense high-energy lofi

All three lofi tracks rank above intense, high-energy songs in other genres, even though their energy is far below the target. The genre weight drives this result.

```text
Intense high-energy lofi
Profile: {'favorite_genre': 'lofi', 'favorite_mood': 'intense', 'target_energy': 0.95, 'likes_acoustic': True}
Top 5 recommendations:
1. Focus Flow
   Score 2.84/4.5: best fit: lofi/intense, genre match (+2.0), mood differs
   (+0.0), energy similarity (+0.45/1.0), acousticness fit (+0.39/0.5).
2. Library Rain
   Score 2.83/4.5: best fit: lofi/intense, genre match (+2.0), mood differs
   (+0.0), energy similarity (+0.40/1.0), acousticness fit (+0.43/0.5).
3. Midnight Coding
   Score 2.82/4.5: best fit: lofi/intense, genre match (+2.0), mood differs
   (+0.0), energy similarity (+0.47/1.0), acousticness fit (+0.35/0.5).
4. Storm Runner
   Score 2.01/4.5: best fit: lofi/intense, genre differs (+0.0), mood match
   (+1.0), energy similarity (+0.96/1.0), acousticness fit (+0.05/0.5).
5. Gym Hero
   Score 2.00/4.5: best fit: lofi/intense, genre differs (+0.0), mood match
   (+1.0), energy similarity (+0.98/1.0), acousticness fit (+0.03/0.5).
```

### Unrepresented genre and mood

With neither `blues` nor `sad` in the catalog, the system still returns recommendations based only on low energy and acousticness; none matches the requested genre or mood.

```text
Unrepresented genre and mood
Profile: {'favorite_genre': 'blues', 'favorite_mood': 'sad', 'target_energy': 0.0, 'likes_acoustic': True}
Top 5 recommendations:
1. Spacewalk Thoughts
   Score 1.18/4.5: best fit: blues/sad, genre differs (+0.0), mood differs
   (+0.0), energy similarity (+0.72/1.0), acousticness fit (+0.46/0.5).
2. Moonlit Waltz
   Score 1.15/4.5: best fit: blues/sad, genre differs (+0.0), mood differs
   (+0.0), energy similarity (+0.69/1.0), acousticness fit (+0.46/0.5).
3. Library Rain
   Score 1.08/4.5: best fit: blues/sad, genre differs (+0.0), mood differs
   (+0.0), energy similarity (+0.65/1.0), acousticness fit (+0.43/0.5).
4. Coffee Shop Stories
   Score 1.07/4.5: best fit: blues/sad, genre differs (+0.0), mood differs
   (+0.0), energy similarity (+0.63/1.0), acousticness fit (+0.45/0.5).
5. Focus Flow
   Score 0.99/4.5: best fit: blues/sad, genre differs (+0.0), mood differs
   (+0.0), energy similarity (+0.60/1.0), acousticness fit (+0.39/0.5).
```

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



