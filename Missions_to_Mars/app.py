from flask import Flask, render_template, redirect
#import config
import scrape_mars as sm

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
from flask_pymongo import PyMongo

# Create an instance of our Flask app.
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# Set route
@app.route('/scrape')
def scrape_insert():
    mars= mongo.db.mars
    mars_data = sm.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)



# Set route
@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)






if __name__ == "__main__":
    app.run(debug=True)
