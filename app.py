from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_mars" 
mongo = PyMongo(app)

@app.route("/")
def home():

    mars = mongo.db.collection.find_one()

    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape_data():

    # Run the scrape function
    news = scrape.scrape_news()
    img = scrape.scrape_img()
    weather = scrape.scrape_weather()
    facts = scrape.scrape_facts()
    img_urls = scrape.scrape_hemispheres()
    
    final_data = {
        "latest_news": news,
        "featured_img": img,
        "weather": weather,
        "facts": facts,
        "img_urls": img_urls
    }

    print(final_data)

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, final_data, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)