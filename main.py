#import the necessary modules
import os
from flask import Flask, render_template, request
from scrape_analysis import connect_service, ret_neu, ret_neg, ret_pos, total_posts

# ininitializing a new Flask web application instance called app
app = Flask(__name__, template_folder='templates', static_folder='static')


# defining a Flask route that maps to the root URL of the web application ("/").
@app.route("/", methods=['GET', 'POST'])
def home():
    # Flask renders the "home.html" template and return the resulting HTML to the user's browser
    return render_template("home.html")

# defining a Flask route that maps to response.html after form processing
@app.route("/response.html", methods=['GET', 'POST'])
def response():
    if request.method == 'POST': #check whether the request method is post
        search = request.form['search_val']#getting the serch value from input field having name search_val
        connect_service(search)  # calling connect_service function of scrape_analysis.py with the search item
        pos = ret_pos()#getting positivity
        search1=search.upper()
        neg = ret_neg()#getting negativity
        
        
        neu = ret_neu()#getting neutrality
        total = total_posts()#getting number of posts examined 
        mylist = [search1, total, pos, neg, neu]#list created to be passed using jinja template to response.html
        path = os.path.join(app.root_path, 'static')#construct a file path to the static directory of the Flask application
    #response.html template rendered with the mylist data and the img_path variable and returned
    return render_template("response.html", mylist=mylist, img_path=path)

#ensuring that the code executes if the script is run as the main program
if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0') #starts the Flask application in debug mode
