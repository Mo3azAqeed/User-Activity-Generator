import faker
import random
import csv
from datetime import datetime, timedelta

# Initialize Faker
fake = faker.Faker()

# Define constants
SUBSCRIPTION_PLANS = {
    "Basic": 9.99,
    "Standard": 14.99,
    "Premium": 19.99
}
PRICE_CHANGE_DATES = {
    datetime(2022, 1, 1): 0.00,
    datetime(2022, 6, 1): 2.50,
    datetime(2023, 1, 1): 1.50,
    datetime(2023, 6, 1): 2.05,
    datetime(2024, 1, 1): 1.50
}
START_DATE = datetime(2021, 1, 1)
END_DATE = datetime.now()

# Generate a price for a given plan based on historical price changes
def get_price_for_plan(plan, date):
    base_price = SUBSCRIPTION_PLANS.get(plan, None)
    if base_price is None:
        raise ValueError(f"Invalid subscription plan: {plan}")

    for change_date, change_amount in sorted(PRICE_CHANGE_DATES.items()):
        if date >= change_date:
            base_price += change_amount

    return round(base_price, 2)

# Function to generate a single price record
def generate_price_record(plan_id, plan, price_date):
    price = get_price_for_plan(plan, price_date)
    price_record = {
        "plan_id": plan_id,
        "plan": plan,
        "price": price,
        "price_date": price_date.isoformat()
    }
    return price_record

# Function to generate and save plan price data to CSV
def generate_plan_prices_csv():
    with open("plan_prices.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "plan_id", "plan", "price", "price_date"
        ])
        writer.writeheader()
        
        # Track plan prices over time
        plan_id = 1
        for plan in SUBSCRIPTION_PLANS.keys():
            for change_date in sorted(PRICE_CHANGE_DATES.keys()):
                price_record = generate_price_record(plan_id, plan, change_date)
                writer.writerow(price_record)
            plan_id += 1

# Function to generate a single random date
def generate_random_date(start, end):
    delta_days = (end - start).days
    return start + timedelta(days=random.randint(0, delta_days))

# Function to generate and save user data to CSV
def generate_user_data_csv(num_users):
    user_data = {}
    with open("user_data.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "user_id", "gender", "age", "interests", "location", "signup_date", "current_plan"
        ])
        writer.writeheader()
        
        for user_id in range(1, num_users + 1):
            gender = random.choice(["Male", "Female", "Non-binary"])
            age = random.randint(18, 70)
            interests = get_user_interests()
            location = fake.city()
            signup_date = generate_random_date(START_DATE, END_DATE)
            current_plan = get_subscription_plan()
            
            user = {
                "user_id": user_id,
                "gender": gender,
                "age": age,
                "interests": interests,
                "location": location,
                "signup_date": signup_date.isoformat(),
                "current_plan": current_plan
            }
            user_data[user_id] = {
                "current_plan": current_plan,
                "signup_date": signup_date
            }
            writer.writerow(user)
    
    return user_data

# Function to generate a random subscription plan
def get_subscription_plan(exclude_plan=None):
    available_plans = list(SUBSCRIPTION_PLANS.keys())
    if exclude_plan:
        available_plans.remove(exclude_plan)
    return random.choice(available_plans)

# Function to generate and save plan change data to CSV
def generate_plan_changes_csv(num_changes, user_data):
    with open("plan_changes.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "change_id", "user_id", "plan", "change_time", "price"
        ])
        writer.writeheader()
        
        # Track user subscriptions and sign-up dates
        for change_id in range(1, num_changes + 1):
            user_id = random.choice(list(user_data.keys()))
            current_plan = user_data[user_id]['current_plan']
            signup_date = user_data[user_id]['signup_date']
            # Ensure the date range for changes is valid
            change_time_start = signup_date + timedelta(days=1)
            if change_time_start >= END_DATE:
                continue
            change_time = generate_random_date(change_time_start, END_DATE)
            new_plan = get_subscription_plan(exclude_plan=current_plan)
            price = get_price_for_plan(new_plan, change_time)
            
            plan_change = {
                "change_id": change_id,
                "user_id": user_id,
                "plan": new_plan,
                "change_time": change_time.isoformat(),
                "price": price
            }
            writer.writerow(plan_change)
            user_data[user_id]['current_plan'] = new_plan

# Function to generate user interests
def get_user_interests():
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
    "Superhero": ["Marvel", "DC", "Independent"] }
    genres = random.sample(list(GENRES.keys()), 3)
    interests = []
    for genre in genres:
        sub_genre = random.choice(GENRES[genre])
        interests.append(f"{genre}: {sub_genre}")
    return '; '.join(interests)
# Generate user data, plan prices, and plan changes
if __name__ == "__main__":
    num_users = 350000
    num_changes = 200000
    user_data = generate_user_data_csv(num_users)
    generate_plan_prices_csv()
    generate_plan_changes_csv(num_changes, user_data)
    print(f"Generated user data for {num_users} users, plan prices, and plan change records for {num_changes} changes.")
