from flask import Flask, send_from_directory

app = Flask(__name__, static_folder="public")

# Serve the game page


@app.route("/")
def index():
    return send_from_directory("public", "tony.html")

# Serve any static files (CSS, JS, JSON, images)


@app.route("/<path:path>")
def static_file(path):
    return send_from_directory("public", path)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
