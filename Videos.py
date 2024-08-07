import random
import csv
from faker import Faker
from datetime import datetime, timedelta

# Constants
GENRES = {
    "Action": ["Superhero", "Martial Arts", "Adventure"],
    "Comedy": ["Stand-Up", "Romantic Comedy", "Satire"],
    "Drama": ["Historical", "Legal", "Family"],
    "Documentary": ["Nature", "Biography", "Science"],
    "Sci-Fi": ["Dystopian", "Space Opera", "Cyberpunk"],
    "Thriller": ["Psychological", "Crime", "Mystery"],
    "Romance": ["Classic", "Contemporary", "Erotic"],
    "Horror": ["Slasher", "Supernatural", "Psychological"],
    "Adventure": ["Fantasy", "Exploration", "Epic"],
    "Fantasy": ["Mythical", "Dark Fantasy", "Urban Fantasy"],
    "Animation": ["3D", "2D", "Stop Motion"],
    "Musical": ["Broadway", "Film Musical", "Concert"],
    "Mystery": ["Whodunit", "Suspense", "Cozy Mystery"],
    "Crime": ["Detective", "Heist", "Legal Drama"],
    "Family": ["Children's", "Teen", "Family Drama"],
    "Historical": ["War", "Ancient", "Medieval"],
    "War": ["Historical War", "Modern War", "Military"],
    "Biography": ["Political", "Entertainment", "Historical"],
    "Reality": ["Competition", "Lifestyle", "Travel"],
    "Game Show": ["Quiz", "Talent", "Reality Competition"],
    "Talk Show": ["Late Night", "Daytime", "Interview"],
    "News": ["Local", "National", "International"],
    "Educational": ["Science", "Math", "Language"],
    "Sport": ["Live", "Documentary", "Highlights"],
    "Lifestyle": ["Cooking", "Home Improvement", "Fitness"],
    "Western": ["Classic", "Modern", "Spaghetti"],
    "Superhero": ["Marvel", "DC", "Independent"]
}

VIDEO_COUNT = 50000
SERIES_RATIO = 0.6  # More series than films
MULTIPLE_SEASONS_RATIO = 0.6  # More series with multiple seasons

# Initialize Faker
fake = Faker()

def generate_video_data():
    video_data = []
    series_data = []
    series_id = 1
    video_id = 1
    series_id_map = {}  # Map video_id to series_id if it's part of a series

    for _ in range(VIDEO_COUNT):
        video_type = 'Film' if random.random() > SERIES_RATIO else 'Series'
        genre = random.choice(list(GENRES.keys()))
        sub_genre = random.choice(GENRES[genre])

        # Generate realistic titles and descriptions
        title = fake.catch_phrase() if video_type == 'Film' else fake.sentence(nb_words=3)
        description = generate_description(genre, sub_genre)

        release_date = fake.date_between(start_date='-5y', end_date='today')
        views = random.randint(1000, 1000000)
        rating = round(random.uniform(1, 5), 1)

        if video_type == 'Film':
            # Check if this film is part of a new series or an existing series
            if random.random() < 0.3 and series_id_map:
                series_id_for_film = random.choice(list(series_id_map.values()))
            else:
                series_id_for_film = None
            
            video_data.append({
                "video_id": video_id,
                "title": title,
                "type": "Film",
                "genre": genre,
                "sub_genre": sub_genre,
                "description": description,
                "release_date": release_date,
                "views": views,
                "rating": rating
            })
            
            if series_id_for_film:
                series_data.append({
                    "series_id": series_id_for_film,
                    "video_id": video_id
                })
                series_id_map[video_id] = series_id_for_film

            video_id += 1
        else:
            # Series
            num_seasons = 1 if random.random() < 0.4 else random.randint(2, 5)
            for season in range(num_seasons):
                num_episodes = random.randint(1, 12)
                for episode in range(num_episodes):
                    episode_title = f"{title} S{season+1}E{episode+1}: " + fake.sentence(nb_words=4)
                    video_data.append({
                        "video_id": video_id,
                        "title": episode_title,
                        "type": "Episode",
                        "genre": genre,
                        "sub_genre": sub_genre,
                        "description": fake.text(max_nb_chars=200),
                        "release_date": release_date,
                        "views": views,
                        "rating": rating
                    })
                    series_data.append({
                        "series_id": series_id,
                        "video_id": video_id,
                        "season_number": season + 1,
                        "episode_number": episode + 1
                    })
                    video_id += 1
            series_id_map[video_id - 1] = series_id  # Map last episode to series_id
            series_id += 1

    return video_data, series_data

def generate_description(genre, sub_genre):
    if genre == "Action":
        return f"An {sub_genre} action-packed adventure."
    elif genre == "Comedy":
        return f"A hilarious {sub_genre} comedy."
    elif genre == "Drama":
        return f"A touching {sub_genre} drama."
    elif genre == "Documentary":
        return f"An informative {sub_genre} documentary."
    elif genre == "Sci-Fi":
        return f"A {sub_genre} science fiction tale."
    elif genre == "Thriller":
        return f"A suspenseful {sub_genre} thriller."
    elif genre == "Romance":
        return f"A romantic {sub_genre} story."
    elif genre == "Horror":
        return f"A terrifying {sub_genre} horror."
    elif genre == "Adventure":
        return f"An exciting {sub_genre} adventure."
    elif genre == "Fantasy":
        return f"A {sub_genre} fantasy tale."
    elif genre == "Animation":
        return f"A beautifully animated {sub_genre} film."
    elif genre == "Musical":
        return f"A {sub_genre} musical performance."
    elif genre == "Mystery":
        return f"A gripping {sub_genre} mystery."
    elif genre == "Crime":
        return f"A {sub_genre} crime drama."
    elif genre == "Family":
        return f"A heartwarming {sub_genre} family story."
    elif genre == "Historical":
        return f"A {sub_genre} historical drama."
    elif genre == "War":
        return f"A {sub_genre} war film."
    elif genre == "Biography":
        return f"A {sub_genre} biography."
    elif genre == "Reality":
        return f"A {sub_genre} reality show."
    elif genre == "Game Show":
        return f"A {sub_genre} game show."
    elif genre == "Talk Show":
        return f"A {sub_genre} talk show."
    elif genre == "News":
        return f"A {sub_genre} news program."
    elif genre == "Educational":
        return f"A {sub_genre} educational series."
    elif genre == "Sport":
        return f"A {sub_genre} sports broadcast."
    elif genre == "Lifestyle":
        return f"A {sub_genre} lifestyle show."
    elif genre == "Western":
        return f"A classic {sub_genre} western."
    elif genre == "Superhero":
        return f"A {sub_genre} superhero saga."
    else:
        return "A captivating story."

def save_to_csv(video_data, series_data):
    with open('videos.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["video_id", "title", "type", "genre", "sub_genre", "description", "release_date", "views", "rating"])
        writer.writeheader()
        writer.writerows(video_data)

    with open('series_relationships.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["series_id", "video_id", "season_number", "episode_number"])
        writer.writeheader()
        writer.writerows(series_data)

if __name__ == "__main__":
    video_data, series_data = generate_video_data()
    save_to_csv(video_data, series_data)
    print(f"Generated {len(video_data)} video records and {len(series_data)} series relationships.")
