# from flask import Flask
from flask import Flask, render_template, flash, request, jsonify
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import requests
import json
import logging
import requests_toolbelt.adapters.appengine

# requests_toolbelt.adapters.appengine.monkeypatch()

try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode


app = Flask(__name__)
GOOGLE_API_KEY = "AIzaSyCrxhYzFUu_gd2PvrYLYOHinmzuIEh3dFM" 
twelth_ave_lat_lon = (39.996643, -83.017430)


class ReusableForm(Form):
    deparature = TextField('deparature', validators=[validators.required()])
    destination = TextField('destination', validators=[validators.required()])
    time = TextField('search_term', validators=[validators.required()])

@app.errorhandler(500)
def server_error(e):
    logging.exception('some error')
    return """
    And internal error <pre>{}</pre>
    """.format(e), 500

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# @app.route('/')
# def hello():
#     return "Hello World!"

def predict(dest_lat, dest_lon, time):
    '''
    Returns a list of possible parking locations around the destination
    which is defined by the dest_lat and dest_lon, as well as the time.

    Example return list: [(-33.556, -32.555), (-33.999, -32.888)]
    '''
    # TODO @ Alex: place your code here and replace the line below with your own return
    # Note: if model only returns one parking location, then just return a list 
    return [(dest_lat, dest_lon)]

def train_model(**kwargs):
    # TODO @ Alex: place training code here, modify function args as needed
    print('Running train_model')

def return_parking_latlon(dest_lat, dest_lon, time='00:00'):
    '''
    dest_lat: Destination latitude
    dest_lon: Destination longitude
    time: Time in 24 hr format, e.g. 17:00 for 5:00 PM
    
    Returns a list of possible parking locations around the destination
    which is defined by the dest_lat and dest_lon, as well as the time.

    Example return list: [(-33.556, -32.555), (-33.999, -32.888)]
    '''
    # TODO @ Alex: Clean time input as you wish, currently is a string of format '00:00'

    # parking_loc_list = TODO @ Alex: Place predict code here
    parking_loc_list = [(dest_lat, dest_lon)]

    # TODO: Remove this example
    parking_loc_list = [twelth_ave_lat_lon]
    return parking_loc_list

@app.route("/map", methods=['POST', 'GET'])
def get_information():
    form = ReusableForm(request.form)
    print (form.errors)

    if request.method == 'POST':
        departure=request.form.get('departure', None)
        departure = departure.replace(' ', '+')

        destination=request.form.get('destination', None)
        destination = destination.replace(' ', '+')

        time=request.form.get('time', None)
        time = time.replace(' ', '+')
        # print(departure)
        # print(destination)
        # print(time)

        response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + departure + '&key=' + GOOGLE_API_KEY)
        resp_json_payload = response.json()
        print("Departure")
        print(resp_json_payload)
        departure_coords = resp_json_payload['results'][0]['geometry']['location']
        departure = str(resp_json_payload['results'][0]['formatted_address'])

        response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + destination + '&key=' + GOOGLE_API_KEY)
        resp_json_payload = response.json()
        print("Destination")
        print(resp_json_payload)
        destination_coords = resp_json_payload['results'][0]['geometry']['location']
        destination = str(resp_json_payload['results'][0]['formatted_address'])

        # gets the parking locations
        parking_loc_list = return_parking_latlon(dest_lat=destination_coords['lat'], dest_lon=destination_coords['lng'], time=time)

        # pass info back to map page
        # init_points = [[departure, departure_coords['lat'], departure_coords['lng'], 'Starting location', 5], [destination, destination_coords['lat'], destination_coords['lng'], 'Ending location', 5]]
        init_points = [(departure_coords['lat'], departure_coords['lng']), (destination_coords['lat'], destination_coords['lng'])]

        # generate google map link // see here: https://developers.google.com/maps/documentation/urls/guide 
        gmap_departure = '{}%2C{}'.format(departure_coords['lat'], departure_coords['lng'])
        gmap_dest = '{}%2C{}'.format(destination_coords['lat'], destination_coords['lng'])
        gmap_waypoints = '{}%2C{}'.format(parking_loc_list[0][0], parking_loc_list[0][1]) # TODO @ Alex: place best parking location here; currently defined as first parking location in the list returned by the return_parking_latlon function
        gmap_parameters = '&origin=' + gmap_departure + '&destination=' + gmap_dest + '&waypoints=' + gmap_waypoints
        gmap_url = 'https://www.google.com/maps/dir/?api=1' + gmap_parameters

        # return render_template('map.html', init_points = init_points, time=time, steps_remaining=steps_remaining, departure=departure, destination=destination)
        return render_template('testmap.html', init_points=init_points, parking_loc_list=parking_loc_list, time=time, departure=departure, destination=destination, gmap_url=gmap_url)

    else:
        return render_template('index.html', form=form)

# @app.route('/<name>')
# def hello_name(name):
#     return "Hello {}!".format(name)

if __name__ == '__main__':
    print('Training model right now.')
    train_model()
    app.run()