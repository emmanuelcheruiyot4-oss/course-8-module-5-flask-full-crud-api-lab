from flask import Flask, jsonify, request

app = Flask(__name__)


# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


# Welcome route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Event Management API"}), 200


# Get all events
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200


# Create a new event
@app.route("/events", methods=["POST"])
def create_event():
    # Get JSON data from the request body.
    data = request.get_json()

    # Validate that JSON data was provided.
    if not data:
        return jsonify({"error": "Request body must contain JSON data."}), 400

    # Validate that the title field exists.
    title = data.get("title")
    if not title:
        return jsonify({"error": "Title is required."}), 400

    # Generate a new ID.
    new_id = max([event.id for event in events], default=0) + 1

    # Create and store the new event.
    new_event = Event(new_id, title)
    events.append(new_event)

    # Return the newly created event.
    return jsonify(new_event.to_dict()), 201


# Update an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    # Find the event with the requested ID.
    for event in events:
        if event.id == event_id:
            # Get JSON data from the request body.
            data = request.get_json()

            # Validate that JSON data was provided.
            if not data:
                return jsonify({"error": "Request body must contain JSON data."}), 400

            # Validate that the title field exists.
            title = data.get("title")
            if not title:
                return jsonify({"error": "Title is required."}), 400

            # Update the event title.
            event.title = title

            # Return the updated event.
            return jsonify(event.to_dict()), 200

    # Event was not found.
    return jsonify({"error": "Event not found."}), 404


# Delete an existing event
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    # Find the event with the requested ID.
    for event in events:
        if event.id == event_id:
            # Remove the event.
            events.remove(event)

            # Return 204 No Content.
            return "", 204

    # Event was not found.
    return jsonify({"error": "Event not found."}), 404


if __name__ == "__main__":
    app.run(debug=True)