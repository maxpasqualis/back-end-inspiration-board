from flask import Blueprint, jsonify, request, make_response
from app import db
from app.models.card import Card
from .helper_functions import get_one_obj_or_abort
import os

card_bp = Blueprint("card_bp", __name__, url_prefix="/cards")

#------------------------POST------------------------------

@card_bp.route("", methods=["POST"])
def add_card():
    request_body = request.get_json()

    if "message" not in request_body:
        return jsonify({"details": "Must have a message"}), 400

    if len(request_body["message"]) > 40:
        return jsonify({"details": "Message must be 40 characters or less"}), 400

    new_card = Card(
        message = request_body["message"]
    )

    db.session.add(new_card)
    db.session.commit()

    print(new_card)
    return jsonify({"message": new_card.create_dict()}), 201

#----------------------GET--------------------------------

@card_bp.route("", methods=["GET"])
def get_all_cards():

    cards = Card.query.all()

    response = [card.create_dict() for card in cards]

    return jsonify(response), 200

@card_bp.route("/<card_id>", methods=["GET"])
def get_one_card(card_id):
    card = get_one_obj_or_abort(Card, card_id)

    return jsonify({"card": card.create_dict()}), 200

#---------------------DELETE-------------------------------

@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_one_card(card_id):
    card = get_one_obj_or_abort(Card, card_id)

    db.session.delete(card)
    db.session.commit()

    return jsonify({"details": f"Card id: {card_id} was deleted"}), 200

#---------------------PATCH---------------------------------
@card_bp.route("/<card_id>", methods=["PATCH"])
def update_likes(card_id):
    card = get_one_obj_or_abort(Card, card_id)
    card.likes_count += 1

    db.session.commit()
    return jsonify({"liked": card.create_dict()})