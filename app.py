from flask import Flask, jsonify, request, send_from_directory
import requests
from geopy.distance import geodesic
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

def get_food_trucks():
    """
    Fetches data about mobile food facilities from the open San Francisco data API
    Returns:
        list: A list of dictionaries containing food truck information
    """
    response = requests.get("https://data.sfgov.org/resource/rqzj-sfat.json")
    return response.json()

def search_by_applicant(name, status=None):
    """
    Searches for food trucks based on the applicant name (case-insensitive)
    Args:
        name (str): Applicant name to search for
        status (str, optional): Filter results by approval status
    Returns:
        list: A list of dictionaries containing matching food truck information
    """
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
    """
    Searches for food trucks based on a partial address search
    Args:
        street_part (str): Part of the street address to search for (case-insensitive)
    Returns:
        list: A list of dictionaries containing matching food truck information
    """
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
    """
    Searches for food trucks closest to the provided user location
    Args:
        latitude (float): User's latitude coordinate
        longitude (float): User's longitude coordinate
        all_status (bool, optional): Include results regardless of approval status (default: False)
    Returns:
        list: A list containing the 5 nearest approved food trucks (or all if all_status is True)
    """
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

# API Endpoints

# Search for food trucks by applicant name
@app.route("/search/applicant", methods=['GET'])
def search_applicant():
    name = request.args.get('name')
    status = request.args.get('status')
    results = search_by_applicant(name, status)
    return jsonify(results)

# Search for food trucks by street location
@app.route("/search/street", methods=['GET'])
def search_street():
    street_part = request.args.get('address')
    results = search_by_street(street_part)
    return jsonify(results)

# Search for food trucks by user location
@app.route("/search/location", methods=['GET'])
def search_location():
    latitude = float(request.args.get('latitude'))
    longitude = float(request.args.get('longitude'))
    all_status = request.args.get('all_status', False) == 'true'
    results = search_by_location(latitude, longitude, all_status)
    return jsonify(results)


@app.route('/')
def serve_index():
    """
    Serve the main HTML file for the frontend.
    """
    return send_from_directory('static', 'index.html')

@app.route('/js/<path:filename>')
def serve_js(filename):
    """
    Serve JavaScript files for the frontend.
    """
    return send_from_directory('static/js', filename)

# Swagger UI configuration
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

    