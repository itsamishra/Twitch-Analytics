from flask import Flask, render_template, jsonify
from scheduled import *
from selector import *
import threading


app = Flask(__name__)

# Reads secet.json
with open("secret.json", "r") as secret_json:
    secret_dict = json.load(secret_json)

# Schedules all scripts
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
