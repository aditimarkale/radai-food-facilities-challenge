from flask import Flask, jsonify, request, send_from_directory
import requests
from geopy.distance import geodesic
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

def get_food_trucks():
    """ Fetches mobile food facilities data from open api"""
    response = requests.get("https://data.sfgov.org/resource/rqzj-sfat.json")
    return response.json()

def search_by_applicant(name, status=None):
    trucks = get_food_trucks()
    results = [
        truck
        for truck in trucks
        if (
            name.lower() in truck['applicant'].lower()
            and (not status or truck['status'] == status)
        )
    ]
    return results

def search_by_street(street_part):
    trucks = get_food_trucks()
    results = [
        truck
        for truck in trucks
        if (
            street_part.lower() in truck['address'].lower()
            and truck['address'].split(' ')[-1].lower().endswith("st")
        )
    ] 
    return results

def search_by_location(latitude, longitude, all_status=False):
    trucks = get_food_trucks()
    if not all_status:
        trucks = [truck for truck in trucks if truck['status'] == "APPROVED"]

    distances = []
    for truck in trucks:
        truck_lat = float(truck['latitude'])
        truck_lon = float(truck['longitude'])
        distance = geodesic((latitude, longitude), (truck_lat, truck_lon)).km
        print(distance)
        distances.append((distance, truck))

    distances.sort(key=lambda x: x[0])
    
    return [truck for _, truck in distances[:5]]

""" API Endpoints """
@app.route("/search/applicant", methods=['GET'])
def search_applicant():
    name = request.args.get('name')
    status = request.args.get('status')
    results = search_by_applicant(name, status)
    return jsonify(results)

@app.route("/search/street", methods=['GET'])
def search_street():
    street_part = request.args.get('address')
    results = search_by_street(street_part)
    return jsonify(results)


@app.route("/search/location", methods=['GET'])
def search_location():
    latitude = float(request.args.get('latitude'))
    longitude = float(request.args.get('longitude'))
    all_status = request.args.get('all_status', False) == 'true'
    results = search_by_location(latitude, longitude, all_status)
    return jsonify(results)


@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('static/js', filename)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Food Trucks API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == "__main__":
    app.run(debug=True)

    