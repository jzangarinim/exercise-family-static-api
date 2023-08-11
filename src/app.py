"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_one_member(id = None):
    if id is not None:
        member = jackson_family.get_member(id)
        if member is not None:
            return jsonify(member), 200
        else:
            return jsonify({"message":"member not found"}), 400

    else:
        return jsonify({"message":"member not found"}), 400

@app.route('/member', methods=['POST'])
def add_one_member():
    data = request.json

    if data.get("first_name") is None:
        return jsonify({"message": "Wrong property"}), 400
    if data.get("age") is None or type(data.get("age")) != int:
        return jsonify({"message": "Wrong property"}), 400
    if data.get("lucky_numbers") is None:
        return jsonify({"message": "Wrong property"}), 400
    if data.get("id") is None:
        data["id"] = None

    member = jackson_family.add_member(data)

    return jsonify(member), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id = None):
    if id is not None:
        member = jackson_family.delete_member(id)
        if member:
            return jsonify({"done": True}), 200
        else:
            return jsonify({"message":"member not found"}), 400

    else:
        return jsonify({"message":"member not found"}), 400

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
