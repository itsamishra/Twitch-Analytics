from pypika import Query, Order
import psycopg2

# Returns all stream records
def get_all_stream_data(twitch_analytics_secrets):
    get_query = (
        Query.from_("stream_data")
        .select("viewer_count", "streamer_name", "streamer_title", "log_time", "rank")
        .orderby("log_time", order=Order.asc)
        .get_sql()
    )

    # Executes SQL query
    db_url = twitch_analytics_secrets["postgres-connection-url"]
    conn = psycopg2.connect(db_url, sslmode="require")
    cur = conn.cursor()
    cur.execute(get_query)

    # Generates & returns top streams list
    top_streams_list = cur.fetchall()
    cur.close()
    conn.close()

    # Creates set of all ranks
    rank_set = set()
    for stream in top_streams_list:
        rank_set.add(stream[4])

    # Initializes rank dictionary
    rank_dict = {}
    for r in rank_set:
        rank_dict[r] = []

    # Adds to rank dictionary
    for stream in top_streams_list:
        rank_dict[stream[4]].append(stream)

    return rank_dict
