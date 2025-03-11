import requests
import mysql.connector

# Database connection settings
DB_CONFIG = {
    "host": "HueyNemud.mysql.pythonanywhere-services.com",
    "user": "HueyNemud",
    "password": "adminadminadmin",
    "database": "HueyNemud$meowiestars",
}

# API URL
API_URL = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/cats-in-movies/records"


def fetch_data():
    """Fetch data from the API."""
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []


def insert_data(records):
    """Insert records into MySQL database."""
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS cats_in_movies (
            id INT AUTO_INCREMENT PRIMARY KEY,
            produced_by VARCHAR(255),
            directed_by VARCHAR(255),
            title VARCHAR(255),
            year VARCHAR(255),
            url_en VARCHAR(255),
            url_poster VARCHAR(255)
        )
    """
    )

    insert_query = """
        INSERT INTO cats_in_movies (produced_by, directed_by, title, year, url_en, url_poster)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    for record in records:
        cursor.execute(
            insert_query,
            (
                record.get("produced_by"),
                record.get("directed_by"),
                record.get("title"),
                record.get("year"),
                record.get("url_en"),
                record.get("url_poster"),
            ),
        )

    connection.commit()
    cursor.close()
    connection.close()


def main():
    data = fetch_data()
    if data:
        insert_data(data)
        print("Data successfully inserted!")
    else:
        print("No data fetched.")


if __name__ == "__main__":
    main()
