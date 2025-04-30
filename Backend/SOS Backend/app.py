from flask import Flask,request,jsonify
import requests
import datetime
import os

app = Flask (__name__)

UPLOAD_FOLDER = r"C:\Users\91995\Desktop\PawPal\PawPal\Backend\SOS Backend\uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def save_image(image):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"image_{timestamp}.jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    image.save(filepath)
    return filename



def get_real_time_location():
    try:
        response= requests.get("https://ipinfo.io/json")
        if response.status_code == 200:
            data = response.json()
            loc = data.get("loc")  # Format: "latitude,longitude"
            if loc:
                lat, lng = loc.split(',')
                return lat, lng
    except Exception as e:
        print(f"Error fetching location: {e}")
    return None,None



@app.route('/donate', methods=['POST'])

def donate():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    amount = data.get("amount")

    if not name or not email or not amount:
        return jsonify({"error": "Missing required fields"}), 400

    if name.isdigit():
        return jsonify({"error": "Invalid name"}), 400

    if "@" not in email or "." not in email:
        return jsonify({"error": "Invalid email address"}), 400

    try:
        amount = float(amount)
        if amount <= 0:
            return jsonify({"error": "Amount must be greater than 0"}), 400
    except ValueError:
        return jsonify({"error": "Amount must be a number"}), 400

    print(f"New Donation Received! \nName: {name} \nEmail: {email} \nAmount: ${amount}")

    return jsonify({"success": True, "message": "Thank you for your donation!"}), 200



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
    
    
    if name.isdigit():
        return jsonify({"error": "Invalid Name"}), 400
    
    
    if not phone.isdigit() or len(phone) != 10:
        return jsonify({"error": "Invalid phone number"}), 400
    
    
    if animal_type not in ["dog", "cat"]:
        return jsonify({"error": "Choose from dog or cat"}), 400
    
    
    if emergency_level not in ["low", "medium", "high"]:
        return jsonify({"error": "Choose from low, medium, high"}), 400
    
    
    if not location:
        lat, lng = get_real_time_location()
        if lat and lng:
            location = f"{lat},{lng}"
        else:
            return jsonify({"error": "Unable to fetch location"}), 400



    print(f"New SOS Alert! \nName: {name} \nPhone: {phone} \nLocation: {location} \nAnimal Type: {animal_type} \nEmergency Level: {emergency_level} \nDescription: {description}")
    
   
    return jsonify({"success": True, "location": location}), 200

@app.route('/support_us/volunteer', methods=['POST'])

def volunteer_support():
    data = request.get_json()

    name = data.get("name","").strip()
    email = data.get("email","").strip()
    phone = data.get("phone","").strip()

    if not name or not email or not phone:
        return jsonify({"error": "Missing required fields"}), 400

    if name.isdigit():
        return jsonify({"error": "Invalid name"}), 400

    if "@" not in email or "." not in email:
        return jsonify({"error": "Invalid email address"}), 400

    if not phone.isdigit() or len(phone) != 10:
        return jsonify({"error": "Invalid phone number"}), 400

    print(f"Interest Submitted! \nName: {name} \nEmail: {email}")

    return jsonify({"success": True, "message": "Thank you for your interest.We will contact you soon"}), 200

@app.route('/quiz', methods=['POST'])

def quiz():
    data= request.get_json()










if __name__ == '__main__':
    app.run(debug=True)
