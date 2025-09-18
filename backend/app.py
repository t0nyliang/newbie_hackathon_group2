from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

# Load JSON data for each member


def load_member_data(member_id):
    filepath = os.path.join("data", f"{member_id}.json")
    with open(filepath, "r") as f:
        return json.load(f)

# Homepage route


@app.route("/")
def home():
    return render_template("index.html")

# Member gallery page


@app.route("/<member_id>")
def member_page(member_id):
    return render_template(f"{member_id}.html")

# API endpoint for member's images


@app.route("/api/<member_id>")
def member_gallery(member_id):
    data = load_member_data(member_id)
    return jsonify(data["images"])


if __name__ == "__main__":
    app.run(debug=True)
