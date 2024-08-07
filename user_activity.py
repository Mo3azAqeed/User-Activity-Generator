import random
from faker import Faker
import csv
import datetime

# Constants
EVENT_TYPE_IDS = {
    "signup": 1,
    "login": 2,
    "browse": 3,
    "search": 4,
    "view": 5,
    "pause": 6,
    "resume": 7,
    "rate": 8,
    "add_to_watchlist": 9,
    "share": 10,
    "subscription_change": 11,
    "feedback": 12
}

SEARCH_TERMS = [
    "action movies", "romantic comedies", "best horror films", "top sci-fi series",
    "latest documentaries", "thriller movies", "classic dramas", "popular sitcoms",
    "new releases", "trending now", "top rated films", "best documentaries",
    "latest episodes of popular series", "movies starring popular actors",
    "shows directed by famous directors", "hidden gems on streaming platforms",
    "films with great reviews", "binge-worthy series", "award-winning movies",
    "highly recommended dramas", "top animated movies", "best family films",
    "guilty pleasure TV shows", "new sci-fi releases", "critically acclaimed documentaries",
    "high tension thrillers", "heartwarming dramas", "horror classics", "nostalgic TV series",
    "best of the decade", "exclusive content on streaming platforms", "latest celebrity interviews",
    "upcoming movie releases", "show recommendations based on genre",
    "must-watch movies before you die", "series finales worth watching", "hidden treasures in genre",
    "user-rated top movies", "best stand-up comedy specials", "latest film reviews",
    "top 10 genre movies", "highly anticipated shows", "best romantic TV shows",
    "under-the-radar films", "genre-bending films", "critically acclaimed TV series",
    "highly rated foreign films", "funniest movies", "best indie films", "top movie franchises",
    "best TV pilots", "hidden gems in genre", "top actors' movies", "best movies of the year"
]

# Read user data from the user_data.csv
def read_user_data(filename='user_data.csv'):
    users = []
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            users.append({
                "user_id": int(row['user_id']),
                "signup_date": datetime.datetime.strptime(row['signup_date'], '%Y-%m-%dT%H:%M:%S')
            })
    return users

# Generate activity records
def generate_user_activity(users, video_ids, num_records=1000000):
    faker = Faker()
    activity_records = []

    def random_date_after_signup(start_date, end_date):
        """Generate a random date between start_date and end_date."""
        return start_date + datetime.timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))

    def generate_search_query():
        return " ".join(random.choices(SEARCH_TERMS, k=random.randint(1, 3)))

    for _ in range(num_records):
        user = random.choice(users)
        user_id = user['user_id']
        session_id = faker.uuid4()
        signup_date = user['signup_date']

        # Session duration and events
        session_start = signup_date
        session_end = session_start + datetime.timedelta(minutes=random.randint(30, 180))  # Sessions last between 30 and 180 minutes

        # Ensure at least two events per session
        num_events = random.randint(2, 20)

        event_times = sorted([random_date_after_signup(session_start, session_end) for _ in range(num_events)])

        for event_time in event_times:
            event_type = random.choice(list(EVENT_TYPE_IDS.keys()))
            event_type_id = EVENT_TYPE_IDS[event_type]
            page_id = None
            search_query = None

            if event_type in ["view", "share", "rate", "add_to_watchlist"]:
                page_id = random.choice(video_ids)
            elif event_type == "search":
                search_query = generate_search_query()
            elif event_type == "pause":
                pause_duration = random.randint(5, 30)  # Pause durations between 5 and 30 minutes
                resume_time = event_time + datetime.timedelta(minutes=pause_duration)
                activity_records.append({
                    "session_id": session_id,
                    "event_type_id": EVENT_TYPE_IDS["pause"],
                    "event_time": event_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "user_id": user_id,
                    "page_id": page_id,
                    "search_query": search_query
                })
                event_time = resume_time  # Resume event happens after pause
            
            activity_records.append({
                "session_id": session_id,
                "event_type_id": event_type_id,
                "event_time": event_time.strftime('%Y-%m-%d %H:%M:%S'),
                "user_id": user_id,
                "page_id": page_id,
                "search_query": search_query
            })

    return activity_records

# Save activity records to CSV
def save_activity_records_to_csv(records, filename='user_activity.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["session_id", "event_type_id", "event_time", "user_id", "page_id", "search_query"])
        writer.writeheader()
        writer.writerows(records)

# Main
if __name__ == "__main__":
    # Load user data
    users = read_user_data()

    # Load video ids from videos.csv
    video_ids = []
    with open('videos.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            video_ids.append(int(row['video_id']))
    
    # Generate user activity data
    activity_records = generate_user_activity(users, video_ids)
    
    # Save to CSV
    save_activity_records_to_csv(activity_records)
    print(f"Generated {len(activity_records)} user activity records.")
