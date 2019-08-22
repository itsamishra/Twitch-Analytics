# TODO: create function that grabs twitch data & run it every 'x' minutes
#   TODO: Make sure that data from function is stored in postgres
# TODO: Move workout-app secret from environment variable to secret.json
# TODO: Add security to database that allows only my ec2's ip to access it (as well as my personal ip)

from flask import Flask
from scheduled import *

app = Flask(__name__)

# Reads secet.json
with open("secret.json", "r") as secret_json:
    secret_dict = json.load(secret_json)

# Schedules all scripts
schedule_scripts(secret_dict)

# Twitch analytics app
@app.route("/project/twitch-analytics/app")
def twitch_analytics_app():

    return "analytics"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
