import csv
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# Define Social Media Channels
SOCIAL_MEDIA_CHANNELS = [
    {"channel_id": 1, "channel_name": "Facebook"},
    {"channel_id": 2, "channel_name": "Instagram"},
    {"channel_id": 3, "channel_name": "X"},
    {"channel_id": 4, "channel_name": "LinkedIn"},
    {"channel_id": 5, "channel_name": "TikTok"},
    {"channel_id": 6, "channel_name": "Snapchat"},
    {"channel_id": 7, "channel_name": "Reddit"},
]

# Define Interaction Types
INTERACTION_TYPES = {
    1: "Click Link",
    2: "View Post",
    3: "Like Post",
    4: "Comment on Post",
    5: "Share Post",
    6: "Save Post",
    7: "Redirect"
}

# Define Marketing Campaigns
CAMPAIGNS = [
    {"campaign_id": 1, "campaign_name": "Summer Sale", "start_date": "2023-06-01", "end_date": "2023-08-31", "budget": 50000, "channel_id": 1},
    {"campaign_id": 2, "campaign_name": "Back to School", "start_date": "2023-08-01", "end_date": "2023-09-30", "budget": 30000, "channel_id": 2},
    {"campaign_id": 3, "campaign_name": "Holiday Special", "start_date": "2023-12-01", "end_date": "2023-12-31", "budget": 70000, "channel_id": 3},
    {"campaign_id": 4, "campaign_name": "New Year Promotions", "start_date": "2024-01-01", "end_date": "2024-01-31", "budget": 60000, "channel_id": 4},
    {"campaign_id": 5, "campaign_name": "Valentine's Day", "start_date": "2024-02-01", "end_date": "2024-02-14", "budget": 40000, "channel_id": 5},
    {"campaign_id": 6, "campaign_name": "Spring Break", "start_date": "2024-03-01", "end_date": "2024-03-31", "budget": 35000, "channel_id": 6},
    {"campaign_id": 7, "campaign_name": "Summer Festival", "start_date": "2024-06-01", "end_date": "2024-08-31", "budget": 55000, "channel_id": 7},
    {"campaign_id": 8, "campaign_name": "Black Friday", "start_date": "2024-11-01", "end_date": "2024-11-30", "budget": 80000, "channel_id": 1},
    {"campaign_id": 9, "campaign_name": "Cyber Monday", "start_date": "2024-12-01", "end_date": "2024-12-31", "budget": 75000, "channel_id": 2},
    {"campaign_id": 10, "campaign_name": "New Year Deals", "start_date": "2024-12-15", "end_date": "2024-12-31", "budget": 40000, "channel_id": 3}
]

# Function to generate random datetime
def random_date(start, end):
    start_datetime = datetime.combine(start, datetime.min.time())
    end_datetime = datetime.combine(end, datetime.max.time())
    return start_datetime + timedelta(days=random.randint(0, (end_datetime - start_datetime).days))

# Generate specific content for posts
def generate_post_content():
    post_types = [
        "New release of the film {}.",
        "User engagement: What's your favorite character in the film {}?",
        "Special offer on {} subscriptions.",
        "Upcoming event: {}.",
        "Poll: Which feature would you like to see next in {}?"
    ]
    film_names = [fake.word() for _ in range(50)]
    topics = [fake.word() for _ in range(50)]
    
    return random.choice(post_types).format(random.choice(film_names + topics))

# Generate Posts
POSTS = []
for i in range(1, 3001):  # 3000 posts
    campaign = random.choice(CAMPAIGNS)
    # Ensure post date is within the campaign's date range
    post_date = random_date(datetime.strptime(campaign["start_date"], "%Y-%m-%d").date(), datetime.strptime(campaign["end_date"], "%Y-%m-%d").date())
    POSTS.append({
        "post_id": i,
        "campaign_id": campaign["campaign_id"],
        "channel_id": campaign["channel_id"],
        "post_content": generate_post_content(),
        "post_date": post_date.date()
    })

# Generate Traffic Data
TRAFFIC_CHANNELS = []

start_date = datetime(2021, 1, 1)
end_date = datetime.now()

# Generate 3 million social media interactions
total_records = 3000000

for i in range(total_records):
    post = random.choice(POSTS)
    post_datetime = datetime.combine(post["post_date"], datetime.min.time())
    if start_date <= post_datetime <= end_date:
        # Ensure most interactions are "Redirect"
        interaction_type_id = 7 if random.random() < 0.6 else random.randint(1, len(INTERACTION_TYPES))
        timestamp = random_date(start_date, end_date).isoformat()
        
        TRAFFIC_CHANNELS.append({
            "interaction_id": i + 1,
            "post_id": post["post_id"],
            "campaign_id": post["campaign_id"],
            "channel_id": post["channel_id"],
            "interaction_type_id": interaction_type_id,
            "timestamp": timestamp,
            "traffic_source": post["channel_id"]
        })

# Function to write CSV files
def write_csv(file_name, data, fieldnames):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Write Campaigns CSV
write_csv('campaigns.csv', CAMPAIGNS, ['campaign_id', 'campaign_name', 'start_date', 'end_date', 'budget', 'channel_id'])

# Write Posts CSV
write_csv('posts.csv', POSTS, ['post_id', 'campaign_id', 'channel_id', 'post_content', 'post_date'])

# Write Social Media Interactions CSV
write_csv('social_media_interactions.csv', TRAFFIC_CHANNELS, ['interaction_id', 'post_id', 'campaign_id', 'channel_id', 'interaction_type_id', 'timestamp', 'traffic_source'])

print("CSV files for campaigns, posts, and social media interactions generated successfully.")
