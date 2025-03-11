from flask import Flask, render_template, jsonify
import requests
import random
import mysql.connector


app = Flask(__name__)

DATASET_URL = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/cats-in-movies/records?limit=100"

DB_CONFIG = {
    "host": "HueyNemud.mysql.pythonanywhere-services.com",
    "user": "HueyNemud",
    "password": "adminadminadmin",  # Ne jamais faire ça en prod
    "database": "HueyNemud$meowiestars",
}


def fetch_dataset_from_api():
    response = requests.get(DATASET_URL)
    if response.status_code == 200:
        data = response.json()
        records = data.get("results", [])
    return records


def fetch_dataset_from_db():
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cat_movies")
    records = cursor.fetchall()
    cursor.close()
    connection.close()
    return records


dataset = fetch_dataset_from_db()


def get_random_cat_movie():
    return random.choice(dataset)


@app.route("/")
def index():
    cat_movie = get_random_cat_movie()
    return render_template("index.html", cat_movie=cat_movie)


@app.route("/random")
def random_cat_movie():
    cat_movie = get_random_cat_movie()
    return jsonify(cat_movie)


if __name__ == "__main__":
    app.run(debug=True)
