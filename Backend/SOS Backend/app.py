from flask import Flask,request,jsonify,render_template,redirect,url_for,session
import requests
import datetime
import os
import random 

app = Flask (__name__)
app.secret_key = 'your_secret_key'



UPLOAD_FOLDER = r"C:\Users\91995\Desktop\PawPal\PawPal\Backend\SOS Backend\uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

for level in ['low','medium','high']:
    os.makedirs(os.path.join(UPLOAD_FOLDER,level),exist_ok=True)

def save_image(image, emergency_level):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"image_{timestamp}.jpg"
    level_folder = os.path.join(UPLOAD_FOLDER, emergency_level.lower())
    filepath = os.path.join(level_folder, filename)
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


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/home')
def home1():
    return render_template('index.html')

@app.route('/contactus')
def contact():
    return render_template('contactus.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')
# @app.route('/donate', methods=['POST'])

# def donate():
#     data = request.   get_json()

#     name = data.get("name")
#     email = data.get("email")
#     amount = data.get("amount")

#     if not name or not email or not amount:
#         return jsonify({"error": "Missing required fields"}), 400

#     if name.isdigit():
#         return jsonify({"error": "Invalid name"}), 400

#     if "@" not in email or "." not in email:
#         return jsonify({"error": "Invalid email address"}), 400

#     try:
#         amount = float(amount)
#         if amount <= 0:
#             return jsonify({"error": "Amount must be greater than 0"}), 400
#     except ValueError:
#         return jsonify({"error": "Amount must be a number"}), 400

#     print(f"New Donation Received! \nName: {name} \nEmail: {email} \nAmount: ${amount}")

#     return jsonify({"success": True, "message": "Thank you for your donation!"}), 200

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
    
    
    if animal_type.lower() not in ["dog", "cat"]:
        return jsonify({"error": "Choose from dog or cat"}), 400

    
    
    if emergency_level.lower() not in ["low", "medium", "high"]:
        return jsonify({"error": "Choose from low, medium, high"}), 400
    
    
    if not location:
        lat, lng = get_real_time_location()
        if lat and lng:
            location = f"{lat},{lng}"
        else:
            return jsonify({"error": "Unable to fetch location"}), 400

    if photo:
        filename = save_image(photo,emergency_level)
        

    print(f"New SOS Alert! \nName: {name} \nPhone: {phone} \nLocation: {location} \nAnimal Type: {animal_type} \nEmergency Level: {emergency_level} \nDescription: {description}")
   
    return redirect(url_for('thank_you'))

@app.route('/thankyou')
def thank_you():
    return render_template('thankyou.html')


# @app.route('/support_us/volunteer', methods=['POST'])

# def volunteer_support():
#     data = request.get_json()

#     name = data.get("name","").strip()
#     email = data.get("email","").strip()
#     phone = data.get("phone","").strip()

#     if not name or not email or not phone:
#         return jsonify({"error": "Missing required fields"}), 400

#     if name.isdigit():
#         return jsonify({"error": "Invalid name"}), 400

#     if "@" not in email or "." not in email:
#         return jsonify({"error": "Invalid email address"}), 400

#     if not phone.isdigit() or len(phone) != 10:
#         return jsonify({"error": "Invalid phone number"}), 400

#     print(f"Interest Submitted! \nName: {name} \nEmail: {email}")

#     return jsonify({"success": True, "message": "Thank you for your interest.We will contact you soon"}), 200


PETS = [
    {
        "name": "Buddy",
        "type": "Dog",
        "breed": "Golden Retriever",
        "age": "2 years",
        "personality": "Friendly, Energetic",
        "ideal_owner": "Active individuals or families with a backyard"
    },
    {
        "name": "Luna",
        "type": "Cat",
        "breed": "Siamese",
        "age": "3 years",
        "personality": "Vocal, Social",
        "ideal_owner": "Someone who spends time at home and wants a talkative companion"
    },
    {
        "name": "Max",
        "type": "Dog",
        "breed": "Labrador Retriever",
        "age": "4 years",
        "personality": "Gentle, Loyal",
        "ideal_owner": "Families with kids or first-time pet owners"
    },
    {
        "name": "Whiskers",
        "type": "Cat",
        "breed": "Tabby",
        "age": "1 year",
        "personality": "Playful, Affectionate",
        "ideal_owner": "Small apartment dwellers or students"
    },
    {
        "name": "Rocky",
        "type": "Dog",
        "breed": "German Shepherd",
        "age": "5 years",
        "personality": "Protective, Smart",
        "ideal_owner": "Experienced dog owners or security-conscious homes"
    },
    {
        "name": "Bella",
        "type": "Cat",
        "breed": "Calico",
        "age": "2 years",
        "personality": "Calm, Independent",
        "ideal_owner": "People who want a low-maintenance companion"
    },
    {
        "name": "Charlie",
        "type": "Dog",
        "breed": "Beagle",
        "age": "1.5 years",
        "personality": "Curious, Cheerful",
        "ideal_owner": "Families who enjoy outdoor activities"
    }
]

@app.route('/quiz', methods=['GET', 'POST'])

def quiz():
    if request.method == 'POST':
        answers = request.form

        # Get user answers from the form
        lifestyle = answers.get('lifestyle')
        home_space = answers.get('home-space')
        time_for_pet = answers.get('time-for-pets')
        pet_experience = answers.get('pet-experience')
        pet_companion = answers.get('pet-companion')

        # Matching logic
        recommended_pet = None

        if lifestyle == 'Active' and home_space == 'Large':
            recommended_pet = "Buddy"
        elif lifestyle == 'Relaxed' and home_space == 'Small':
            recommended_pet = "Whiskers"
        elif pet_experience == 'Beginner' and pet_companion == 'Companion':
            recommended_pet = "Max"
        elif lifestyle == 'Active' and pet_companion == 'Companion':
            recommended_pet = "Charlie"
        elif pet_experience == 'Experienced' and home_space == 'Large':
            recommended_pet = "Rocky"
        else:
            recommended_pet = random.choice([pet['name'] for pet in PETS])

        pet = next((pet for pet in PETS if pet['name'] == recommended_pet), None)

        if pet:
            session['pet'] = pet  # Save to session
            return redirect(url_for('result'))
        else:
            return "No matching pet found", 400

    return render_template('quiz.html')

@app.route('/result')
def result():
    pet = session.get('pet')
    if not pet:
        return redirect(url_for('quiz'))
    return render_template('result.html', pet=pet)












@app.route('/meet-pets')
def meet_pets():
    return render_template('meet-pets.html')


@app.route('/search_pets', methods=['GET','POST'])
def search_pets():
    pets = [
        {
            "name": "Buddy",
            "type": "Dog",
            "age": "2 years",
            "gender": "Male",
            "breed": "Golden Retriever",
            "description": "Buddy is a friendly and energetic dog who loves playing fetch and going for walks."
        },
        {
            "name": "Whiskers",
            "type": "Cat",
            "age": "1 year",
            "gender": "Female",
            "breed": "Tabby",
            "description": "Whiskers is a sweet and playful cat who loves to cuddle and chase toys around the house."
        },
        {
            "name": "Max",
            "type": "Dog",
            "age": "3 years",
            "gender": "Male",
            "breed": "Labrador",
            "description": "Max is a gentle and friendly dog who gets along well with children and other pets."
        },
        {
            "name": "Bella",
            "type": "Cat",
            "age": "2 years",
            "gender": "Female",
            "breed": "Calico",
            "description": "Bella is a calm and affectionate cat who enjoys lounging in sunny spots and gentle pets."
        },
        {
            "name": "Rocky",
            "type": "Dog",
            "age": "4 years",
            "gender": "Male",
            "breed": "German Shepherd",
            "description": "Rocky is an intelligent and loyal dog who loves to learn new tricks and commands."
        },
        {
            "name": "Luna",
            "type": "Cat",
            "age": "3 years",
            "gender": "Female",
            "breed": "Siamese",
            "description": "Luna is a vocal and social cat who enjoys being the center of attention."
        },
        {
            "name": "Charlie",
            "type": "Dog",
            "age": "1 year",
            "gender": "Male",
            "breed": "Beagle",
            "description": "Charlie is a curious and friendly puppy who loves exploring and meeting new people."
        },
        {
            "name": "Lily",
            "type": "Cat",
            "age": "2 years",
            "gender": "Female",
            "breed": "Persian",
            "description": "Lily is a gentle and laid-back cat who enjoys quiet time and gentle pets."
        }
    ]
    return jsonify(pets)







if __name__ == '__main__':
    app.run(debug=True)
