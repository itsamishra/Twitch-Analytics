# DONE: create function that grabs twitch data & run it every 10 seconds
#   DONE: Make sure that data from function is stored in postgres
#   DONE: Add function to scheduler that runs function every 10 seconds
# TODO: Add function that delets all records >24 hours old
# TODO: Add front end that uses stream data
# TODO: Move workout-app secret from environment variable to secret.json
# TODO: Add security to database that allows only my ec2's ip to access it (as well as my personal ip)

from flask import Flask, render_template, jsonify
from scheduled import *
from selector import *
import threading


app = Flask(__name__)

# Reads secet.json
with open("secret.json", "r") as secret_json:
    secret_dict = json.load(secret_json)

# Schedules all scripts
# schedule_scripts(secret_dict)
thread = threading.Thread(target=schedule_scripts, args=(secret_dict,))
thread.start()

# Returns stream data
@app.route("/project/twitch-analytics/api/get-stream-data")
def get_stream_data_api():
    stream_data = get_all_stream_data(secret_dict["twitch-analytics"])

    return jsonify(stream_data)


# Twitch analytics app
@app.route("/project/twitch-analytics/app")
def twitch_analytics_app():
    return render_template("twitch-analytics-app.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
