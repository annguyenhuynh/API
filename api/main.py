from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#----Create database-----
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///travel.db"

db = SQLAlchemy(app)

class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "destination": self.destination,
            "country": self.country,
            "rating": self.rating
        }

with app.app_context():
    db.create_all()

#----Create routes-----

#Home page: https://www.thenerdnook.io/
@app.route("/")
def home():
    return jsonify({"message":"Welcome to Travel API"})

#Destination: https://www.thenerdnook.io/destinations
@app.route("/destinations", methods=["GET"])
def get_destinations():
    destinations = Destination.query.all()

    return jsonify([destination.to_dict() for destination in destinations])

#Get specific destination: #Destination: https://www.thenerdnook.io/destinations/<id>
@app.route("/detinations/<int:destination_id>", methods=["GET"])
def get_destination(desination_id):
    destination=Destination.query.get(desination_id)
    if destination:
        return jsonify(destination.to_dict())
    else:
        return jsonify({"error":"Destination not found"}), 404
#POST
@app.route("/destinations", methods=["POST"])
def add_destination():  
    data = request.get_json() 

    new_destination=Destination(destination=data["destination"],
                                country=data["country"],
                                rating=data["rating"])
    db.session.add(new_destination)
    db.session.commit()

    return jsonify(new_destination.to_dict()), 201

# PUT --> Update
@app.route("/destinations/<int:destination_id>", methods=["PUT"])
def update_destination(destination_id):
    data = request.get_json()

    destination=Destination.query.get(destination_id)
    if destination:
        destination.destination=data.get("destination", destination.destination)
        destination.country=data.get("country", destination.country)
        destination.rating=data.get("rating", destination.rating)

        db.session.commit()

        return jsonify(destination.to_dict())
    else:
        return jsonify ({"error":"Destination not found"}), 404
    
# DELETE 
@app.route("/destinations/<int:destination_id>", methods=["DELETE"])
def delete_destination(destination_id):
    destination=Destination.query.get(destination_id)
    if destination:
        db.session.delete(destination)
        db.session.commit()

        return jsonify({"message":"destination was deleted"})
    else:
        return jsonify ({"error":"Destination not found"}), 404
        


if __name__ == "__main__":
    app.run(debug=True)