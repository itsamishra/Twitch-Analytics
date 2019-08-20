from flask import Flask

app = Flask(__name__)


# Twitch analytics app
@app.route("/project/twitch-analytics/app")
def twitch_analytics_app():
    return "analytics"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
