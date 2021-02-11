from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Creating an instance of Flask
app = Flask(__name__)

# Using PyMongo to establish Mongo connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

#connecting to mongo db
db = client.Mission_to_Mars
mars_data = db.mars_data



@app.route("/")
def home():
    mars = db.mars_data.find_one()
    return render_template('index.html', mars=mars)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_scraped_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)