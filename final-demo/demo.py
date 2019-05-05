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


class ReusableForm(Form):
    deparature = TextField('deparature', validators=[validators.required()])
    destination = TextField('destination', validators=[validators.required()])
    search_term = TextField('search_term', validators=[validators.required()])

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

@app.route("/map", methods=['POST', 'GET'])
def get_information():
    form = ReusableForm(request.form)
    print (form.errors)

    if request.method == 'POST':
        departure=request.form['departure']
        departure = departure.replace(' ', '+')

        destination=request.form['destination']
        destination = destination.replace(' ', '+')

        search_term=request.form['search_term']
        search_term = search_term.replace(' ', '+')
        # print(departure)
        # print(destination)
        # print(search_term)

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

        # pass first and last position info
        # init_points = [[departure, departure_coords['lat'], departure_coords['lng'], 'Starting location', 5], [destination, destination_coords['lat'], destination_coords['lng'], 'Ending location', 5]]
        init_points = [[departure_coords['lat'], departure_coords['lng']], [destination_coords['lat'], destination_coords['lng']]]

        # return render_template('map.html', init_points = init_points, search_term=search_term, steps_remaining=steps_remaining, departure=departure, destination=destination)
        return render_template('testmap.html', init_points=init_points, search_term=search_term, departure=departure, destination=destination)

    else:
        return render_template('index.html', form=form)

@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

if __name__ == '__main__':
    app.run()