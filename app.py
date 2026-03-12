from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample in-memory data for hotels and bookings
hotels = [
    {"id": 1, "name": "Grand Palace", "location": "Manila", "rooms": 10},
    {"id": 2, "name": "Sea View Resort", "location": "Cebu", "rooms": 5},
]

bookings = [
    {"id": 1, "hotel_id": 1, "guest_name": "Juan", "nights": 3},
    {"id": 2, "hotel_id": 2, "guest_name": "Maria", "nights": 2},
]

# ------------------ Home ------------------
@app.route('/')
def home():
    return "Welcome to the Hotel Booking API!"

# ------------------ List all hotels ------------------
@app.route('/hotels', methods=['GET'])
def list_hotels():
    return jsonify(hotels)

# ------------------ Get hotel by ID ------------------
@app.route('/hotel/<int:id>', methods=['GET'])
def get_hotel(id):
    hotel = next((h for h in hotels if h["id"] == id), None)
    if not hotel:
        return jsonify({"error": "Hotel not found"}), 404
    return jsonify(hotel)

# ------------------ Add a new hotel ------------------
@app.route('/hotel', methods=['POST'])
def add_hotel():
    data = request.get_json()
    if not data or not all(k in data for k in ("name", "location", "rooms")):
        return jsonify({"error": "Missing fields"}), 400
    new_id = len(hotels) + 1
    hotel = {
        "id": new_id,
        "name": data["name"],
        "location": data["location"],
        "rooms": data["rooms"]
    }
    hotels.append(hotel)
    return jsonify({"message": "Hotel added successfully", "hotel": hotel}), 201

# ------------------ Update hotel ------------------
@app.route('/hotel/<int:id>', methods=['PUT'])
def update_hotel(id):
    hotel = next((h for h in hotels if h["id"] == id), None)
    if not hotel:
        return jsonify({"error": "Hotel not found"}), 404
    data = request.get_json()
    hotel["name"] = data.get("name", hotel["name"])
    hotel["location"] = data.get("location", hotel["location"])
    hotel["rooms"] = data.get("rooms", hotel["rooms"])
    return jsonify({"message": "Hotel updated", "hotel": hotel})

# ------------------ Delete hotel ------------------
@app.route('/hotel/<int:id>', methods=['DELETE'])
def delete_hotel(id):
    global hotels
    hotel = next((h for h in hotels if h["id"] == id), None)
    if not hotel:
        return jsonify({"error": "Hotel not found"}), 404
    hotels = [h for h in hotels if h["id"] != id]
    return jsonify({"message": "Hotel deleted", "hotel": hotel})

# ------------------ List all bookings ------------------
@app.route('/bookings', methods=['GET'])
def list_bookings():
    return jsonify(bookings)

# ------------------ Add a new booking ------------------
@app.route('/booking', methods=['POST'])
def add_booking():
    data = request.get_json()
    if not data or not all(k in data for k in ("hotel_id", "guest_name", "nights")):
        return jsonify({"error": "Missing fields"}), 400
    hotel = next((h for h in hotels if h["id"] == data["hotel_id"]), None)
    if not hotel:
        return jsonify({"error": "Hotel not found"}), 404
    if data["nights"] <= 0:
        return jsonify({"error": "Nights must be greater than 0"}), 400
    new_id = len(bookings) + 1
    booking = {
        "id": new_id,
        "hotel_id": data["hotel_id"],
        "guest_name": data["guest_name"],
        "nights": data["nights"]
    }
    bookings.append(booking)
    return jsonify({"message": "Booking added", "booking": booking}), 201

# ------------------ Get bookings by hotel ------------------
@app.route('/bookings/<int:hotel_id>', methods=['GET'])
def get_bookings_by_hotel(hotel_id):
    hotel = next((h for h in hotels if h["id"] == hotel_id), None)
    if not hotel:
        return jsonify({"error": "Hotel not found"}), 404
    hotel_bookings = [b for b in bookings if b["hotel_id"] == hotel_id]
    return jsonify(hotel_bookings)

# ------------------ Delete booking ------------------
@app.route('/booking/<int:id>', methods=['DELETE'])
def delete_booking(id):
    global bookings
    booking = next((b for b in bookings if b["id"] == id), None)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404
    bookings = [b for b in bookings if b["id"] != id]
    return jsonify({"message": "Booking deleted", "booking": booking})

# ------------------ Run the app ------------------
if __name__ == '__main__':
    app.run(debug=True)
