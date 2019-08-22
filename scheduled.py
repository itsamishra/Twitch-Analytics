# Contains all scheduled scripts

import requests
import json
from pypika import Query, Table
import psycopg2
import datetime

# Schedules functions to run at appropriate time intervals
def schedule_scripts(secret_dict):
    print("scheduling...")
    twitch_analytics_secrets = secret_dict["twitch-analytics"]
    get_twitch_viewership_data(twitch_analytics_secrets)


# Retreives top 20 streams from Twitch API and inserts them into db
def get_twitch_viewership_data(twitch_analytics_secrets):
    endpoint = "https://api.twitch.tv/helix/streams?first=10"
    headers = {"Client-Id": twitch_analytics_secrets["twitch-client-id"]}
    top_streams = []

    # Makes API call and creates list of top streams
    r = requests.get(endpoint, headers=headers)
    for raw_stream_data in r.json()["data"]:
        stream_data = {
            "viewer_count": raw_stream_data["viewer_count"],
            "streamer_name": raw_stream_data["user_name"],
            "stream_title": raw_stream_data["title"],
            "started_at": raw_stream_data["started_at"],
        }
        top_streams.append(stream_data)

    # Creates SQL query
    stream_data = Table("stream_data")
    insert_stream_data_query = Query.into(stream_data).columns(
        "viewer_count", "streamer_name", "streamer_title", "log_time"
    )
    timestamp = str(datetime.datetime.now())
    for stream in top_streams:
        insert_stream_data_query = insert_stream_data_query.insert(
            stream["viewer_count"], stream["streamer_name"], stream["stream_title"], timestamp
        )
    insert_stream_data_query = insert_stream_data_query.get_sql()

    # Executes SQL query
    db_url = twitch_analytics_secrets["postgres-connection-url"]
    conn = psycopg2.connect(db_url, sslmode="require")
    cur = conn.cursor()
    cur.execute(insert_stream_data_query)
    conn.commit()

    # Closes cursor and connection
    cur.close()
    conn.close()
