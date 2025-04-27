from flask import Flask 
from flask import request,jsonify
import requests

app = Flask (__name__)

def get_real_time_location(api_key):
    url="https://www.googleapis.com/geolocation/v1/geolocate?key= +{api_key}"
    response=requests.post(url)

    if response.status_code==200:
        data= response.json()
        location=data.get("location")
        if location:
            return location['lat'],location['lng']
    return None,None


@app.route('/submit_sos', methods=['POST'])
def submit_sos():
    data = request.get_json()

    name = data.get("name")
    phone = data.get("phone")
    location = data.get("location")
    animal_type = data.get("animal_type")
    emergency_level = data.get("emergency_level")
    description = data.get("description")

    # Check for missing fields
    if name is None or phone is None or animal_type is None or emergency_level is None or description is None:
        return jsonify({"error": "Missing required fields"}), 400
    
    # Validate name
    if name.isdigit():
        return jsonify({"error": "Invalid Name"}), 400
    
    # Validate phone number
    if not phone.isdigit() or len(phone) != 10:
        return jsonify({"error": "Invalid phone number"}), 400
    
    # Validate animal type
    if animal_type not in ["dog", "cat"]:
        return jsonify({"error": "Choose from dog or cat"}), 400
    
    # Validate emergency level
    if emergency_level not in ["low", "medium", "high"]:
        return jsonify({"error": "Choose from low, medium, high"}), 400
    
    # Handle location if it's not provided
    if not location:
        api_key = "YOUR_GOOGLE_API_KEY"  # Replace with your actual API key
        lat, lng = get_real_time_location(api_key)
        if lat and lng:
            location = f"{lat}, {lng}"
        else:
            return jsonify({"error": "Unable to fetch location"}), 500
    
    # Log the received data
    print(f"New SOS Alert! \nName: {name} \nPhone: {phone} \nLocation: {location} \nAnimal Type: {animal_type} \nEmergency Level: {emergency_level} \nDescription: {description}")
    
    # Respond with success
    return jsonify({"success": True, "location": location}), 200


if __name__ == '__main__':
    app.run(debug=True)