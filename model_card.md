# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**Find Your Rhythm**

---

## 2. Intended Use  

This simulation suggests songs that fit a listener's stated preferences. It assumes the listener can choose a genre, mood, energy level, and acoustic preference. It is for classroom exploration, not a production music service.

---

## 3. How the Model Works  

The recommender compares each song with the listener's preferred genre, mood, energy level, and acoustic sound. Matching genre and mood each earn points, and songs gain additional points when their energy and acousticness fit the listener's preferences. In the current weight-shift experiment, energy similarity can earn twice as many points as either a genre or mood match. Genre and mood must match exactly; energy is rewarded for being close to the target, not simply for being high.

The listener can describe more than one taste, such as intense rock and chill lofi. The system scores each song against each taste, keeps the best score, and recommends the highest-scoring songs with reasons for their scores. Unlike the starter logic, which returned songs in their original order, this approach ranks them by how well they match. It uses song attributes rather than other listeners' behavior.

---

## 4. Data  

The catalog has 18 songs: 10 starter songs and 8 added songs. It includes genres such as pop, lofi, rock, folk, and salsa, and moods such as happy, chill, intense, and dreamy. Each song also has numerical features such as energy and tempo. The data does not include lyrics, listening history, or every genre and mood.

---

## 5. Strengths  

The system works well when the catalog contains songs close to a listener's stated taste. For example, it ranks *Sunrise City* first for high-energy pop and *Library Rain* first for chill lofi. It also explains which features contributed to each score.

---

## 6. Limitations and Bias 

The recommender struggles when a listener's preferred genre or mood is absent from the catalog. In the baseline experiment with a blues/sad profile, neither label appeared in the dataset, so the top results matched neither preference. The system still ranked songs using energy and acousticness, which could give a misleading impression that they fit the listener's overall taste. This particularly disadvantages people whose preferred styles or moods are underrepresented in the small catalog.

---

## 7. Evaluation  

I compared the top five recommendations for three profiles using the current weights: High-Energy Pop (happy and energetic), Chill Lofi (chill and lower-energy), and Deep Intense Rock (intense and energetic). I checked whether the songs' styles and energy fit each profile. Earlier baseline experiments also tested conflicting and unavailable preferences, as documented in the README.

- **Pop vs. lofi:** Pop recommends *Sunrise City* first, while lofi recommends *Library Rain*. This makes sense because the profiles favor different genres, energy levels, and acoustic sounds.
- **Pop vs. rock:** Pop puts *Sunrise City* first; rock puts *Storm Runner* first. Both include *Gym Hero*: it is pop, but its intense mood and high energy also suit the rock profile.
- **Lofi vs. rock:** Lofi favors *Library Rain* and *Midnight Coding*, while rock favors *Storm Runner* and *Gym Hero*. The lofi profile prefers calmer, more acoustic songs, whereas the rock profile favors more energy and less acoustic sound.

One surprise was that *Gym Hero* ranks third for someone seeking happy pop, even though its mood is labeled intense. Its pop genre, high energy, and low acousticness still earn enough points to make it a strong match. That shows how a song can rank highly without matching every preference, but it does not prove the listener will actually like it.

---

## 8. Future Work  

Add more songs and represent more genres and moods. Let listeners set preferences for tempo and danceability, and allow neutral acoustic preferences. Explore related genres and moods instead of requiring exact matches. Test ways to include more than one style in the top results, then ask listeners whether the suggestions are useful.

---

## 9. Personal Reflection  

This project shows how a few choices about points can change a recommendation list. It was surprising that a song labeled intense could rank highly for a happy-pop profile because its other features matched. A high score is only an estimate, not proof that someone will enjoy a song.
