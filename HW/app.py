from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#  create route that renders index.html template
@app.route("/")
def index():
    mars_collection = mongo.db.mars_collection.find_one()
    return render_template("index.html", mars_collection=mars_collection)


@app.route("/scrape")
def scrape():
    mars_collection = mongo.db.mars_collection
    mars_data = scrape_mars.scrape()
    mars_collection.update({}, mars_data, upsert=True )
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)