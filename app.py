import os
import openai
import tweepy
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta
from random import randint

load_dotenv()

X_API_KEY = os.environ.get("X_API_KEY")
X_API_KEY_SECRET = os.environ.get("X_API_KEY_SECRET")
X_BEARER_TOKEN = os.environ.get("X_BEARER_TOKEN")
X_ACCESS_TOKEN = os.environ.get("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = os.environ.get("X_ACCESS_TOKEN_SECRET")

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL")
PROMPT = os.environ.get("PROMPT")

client = tweepy.Client(bearer_token=X_BEARER_TOKEN, consumer_key=X_API_KEY, consumer_secret=X_API_KEY_SECRET,
                       access_token=X_ACCESS_TOKEN, access_token_secret=X_ACCESS_TOKEN_SECRET)


def generate_post(openai_api_key, model, prompt):
    openai.api_key = openai_api_key
    try:
        completions = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        message = completions.choices[0].message.content
        print(message)
    except Exception as e:
        message = f'API Error: {str(e)}'
    return message


def publish(post):
    try:
        client.create_tweet(text=post)
        print("Published:", post)
    except Exception as e:
        print("Error:", e)


def scheduled_tweet():
    post = generate_post(OPENAI_API_KEY, OPENAI_MODEL, PROMPT)
    if post:
        publish(post)


def random_time_in_range(start_hour, start_minute, end_hour, end_minute):
    start_time = datetime.now().replace(
        hour=start_hour, minute=start_minute, second=0, microsecond=0)
    end_time = datetime.now().replace(
        hour=end_hour, minute=end_minute, second=0, microsecond=0)
    delta = end_time - start_time
    random_seconds = randint(0, delta.seconds)
    random_time = start_time + timedelta(seconds=random_seconds)
    return random_time


if __name__ == "__main__":
    scheduler = BlockingScheduler()

    # Schedule tweet for a random time between 10:30 AM to 12:00 PM
    morning_time = random_time_in_range(10, 30, 12, 0)
    scheduler.add_job(scheduled_tweet, 'interval',
                      days=1, next_run_time=morning_time)

    # Schedule tweet for a random time between 5:30 PM to 7:00 PM
    evening_time = random_time_in_range(17, 30, 19, 0)
    scheduler.add_job(scheduled_tweet, 'interval',
                      days=1, next_run_time=evening_time)

    # Start the scheduler
    scheduler.start()
