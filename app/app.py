from flask import Flask, render_template, jsonify
import psycopg2

app = Flask(__name__,template_folder='templates')

# Database configuration
DB_HOST = "db"
DB_NAME = "listings"
DB_USER = "root"
DB_PASS = "pass"
DB_PORT = "5432"


@app.route('/')
def index():
    return render_template('index.html')

"""@app.route('/')
def index():
    # Connect to the database
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )

    # Fetch data from the listings table
    cur = conn.cursor()
    cur.execute("SELECT title, image_url FROM listings")
    listings = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('index.html', listings=listings)"""

@app.route('/get_listings')
def get_listings():
    # Connect to the database
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )

    # Fetch data from the listings table
    cur = conn.cursor()
    cur.execute("SELECT title, image_url FROM listings")
    listings = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(listings=listings)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
