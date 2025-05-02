from flask import Flask,request,jsonify
import requests
import datetime
import os
from flask import render_template
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

@app.route('/sos-report', methods=['GET', 'POST'])
def sos_report():
    return render_template('sos-report.html')


@app.route('/submit_sos', methods=['POST'])

def submit_sos():
    name = request.form.get("name")
    phone = request.form.get("phone")
    location = request.form.get("location")
    animal_type = request.form.get("animal_type")
    emergency_level = request.form.get("emergency_level")
    description = request.form.get("description")
    photo = request.files.get("photo")  # For file input


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

    if photo:
        filename = save_image(photo)
        

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
    return jsonify({"success": True, "message": "Quiz received"}), 200
PETS = [
    {
        "name": "Buddy",
        "type": "dog",
        "age": "2 years",
        "gender": "male",
        "breed": "Golden Retriever",
        "description": "Buddy is a friendly and energetic dog who loves playing fetch and going for walks."
    },
    {
        "name": "Whiskers",
        "type": "cat",
        "age": "1 year",
        "gender": "female",
        "breed": "Tabby",
        "description": "Whiskers is a sweet and playful cat who loves to cuddle and chase toys around the house."
    },
    # ... Add other pets similarly
]

@app.route('/search_pets', methods=['GET'])
def search_pets():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify(PETS)
    
    filtered = [pet for pet in PETS if query in pet["name"].lower() or query in pet["breed"].lower()]
    return jsonify(filtered)










if __name__ == '__main__':
    app.run(debug=True)
