from flask import Flask 
from flask import request,jsonify

app = Flask (__name__)
@app.route('/submit_sos', methods=['POST'])

def submit_sos():
    data=request.get_json()
    if name is None or phone is None or location is None or animal_type is None or emergency_level is None or description is None:
        return jsonify({"error":"Missing required fields"}) 
    else: 

        name=data.get("name")
        if name.isdigit():
            return jsonify({"error":"Invalid Name"})
        
        phone=data.get("phone")
        if not phone.isdigit() or phone!=10:
            return jsonify({"error":"Invalid phone number"})
        
        location=data.get("location")
        #option: dog, cat
        animal_type=data.get("animal_type")
        if animal_type not in ["dog", "cat"]:
            return jsonify({"error":"Choose from dog or cat"})

        #choose from low medium high
        emergency_level=data.get("emergency_level")
        if emergency_level not in ["low", "medium", "high"]:
            return jsonify({"error":"Choose from low,medium,high"})

        description=data.get("description")
        print(f"New SOS Alert! \nName: {name} \nPhone: {phone} \nLocation: {location} \nAnimal Type: {animal_type} \nEmergency Level: {emergency_level} \nDescription: {description}")

        return jsonify({"success":True}), 200

if __name__ == '__main__':
    app.run(debug=True)
    