from flask import Flask, render_template, request, redirect
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import pyrebase

# Setup for Firebase
config = {
  "apiKey": "[KEY]",
  "authDomain": "pot-holing.firebaseapp.com",
  "databaseURL": "https://pot-holing.firebaseio.com",
  "storageBucket": "pot-holing.appspot.com"
}

# Initialise Firebase
firebase = pyrebase.initialize_app(config)

# Get access to firebase's components
auth = firebase.auth()
database = firebase.database()
storage = firebase.storage()

# user = auth

# Setup for Flask
app = Flask(__name__)

# Setup for Google Maps
app.config['GOOGLEMAPS_KEY'] = "[KEY]"
GoogleMaps(app)

# Colours to be used to mark the different categories
category_colour = {
    "Pothole": 'FF0000',
    "Overflowing Bin": 'FFA500',
    "Streerlight Out": 'FFFF00',
    "Vandalism": '00FF00',
    "Fly Tipping": '00FFA5',
    "Dog Waste": '0000FF',
    "Uncollected Bins": 'FF00FF',
    "Parking Offenses": 'FFC0CB',
    "Abandoned Vehicles": '00FFFF',
    "Other": 'EE82EE'
}

reports = []
markers = []


# Class Object to match the original Java report object stored in the database
class Report:
    def __init__(self, category, description, img_ref, lat, long, owner, time):
        self.category = category            # Type of report
        self.description = description      # Description of Issue
        self.img_ref = img_ref              # Reference to the image in storage
        self.lat = lat                      # Latitude of report
        self.long = long                    # Longitude of report
        self.owner = owner                  # Poster of report
        self.time = time                    # Time of report

        # Additional Members used only by this application
        self.icon = ""                      # Icon for Marker
        self.url = ""                       # URL for image


# Handle the opening of the main map page
@app.route('/')
def map_page():

    global reports
    global auth

    # Check if the user is logged in
    if auth.current_user is None:
        print("Not Logged In")

    # If there are no reports, load them
    if not reports:
        # Retrieve the list of reports from the database
        unprocessed = database.child("reports").get().val()

        # Take the returned data and convert it into Report objects
        processed = []
        for report in unprocessed:
            current_report = unprocessed[report]
            processed.append(Report(current_report["category"],
                                    current_report["description"],
                                    current_report["imgRef"],
                                    current_report["lat"],
                                    current_report["long"],
                                    current_report["owner"],
                                    current_report["time"]))

        # Turn the list of report objects in to a list of markers to be placed on the map
        for report in processed:
            report.url = storage.child("images/" + report.img_ref).get_url(None)
            report_w_icon = build_icon(report)
            reports.append(report_w_icon)

    # Construct the map
    g_map = Map(
        varname="mapInstance",
        identifier="gMap",
        lat=37.4419,
        lng=-122.1419,
        style="width:100%;height:100%;margin:0",
        center_on_user_location=True,
        fullscreen_control=False,
        maptype_control=False,
        streetview_control=False
    )

    # Render the map
    return render_template('main.html', gMap=g_map, reports=reports)


# Construct the icon to be placed on the map
def build_icon(report):
    # Base url for the marker
    icon = "http://www.googlemapsmarkers.com/v1/"

    # Get the category of the report
    category = report.category

    # Check if the category has an assigned colour
    if category in category_colour:
        # If yes, add the colour to the icon request string
        icon += category_colour[category] + "/"
    else:
        # If no, make the icon black
        icon += "000000/"

    # Set the icon
    report.icon = icon

    # Return the completed marker
    return report


# Handle the opening of the about page
@app.route('/about/')
def about():
    return render_template('about.html')


# Handle the opening of the login page
@app.route('/login/')
def login():
    return render_template('login.html')


# Handle attempts to login
@app.route('/handle_login', methods=['POST'])
def handle_login():
    global auth

    form = request.form
    username = form['uname']
    password = form['psw']

    auth.sign_in_with_email_and_password(username, password)

    if auth.current_user is not None:
        print("success")

    return redirect('/')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
