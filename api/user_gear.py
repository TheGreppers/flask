"""
User Gear API — CRUD for per-user racing equipment tracking.

Endpoints:
    GET    /api/sfi/gear       — list current user's gear
    POST   /api/sfi/gear       — add a gear item
    DELETE /api/sfi/gear/<id>  — remove a gear item
"""

from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from api.authorize import token_required
from model.user_gear import UserGear

user_gear_api = Blueprint('user_gear_api', __name__, url_prefix='/api/sfi')
api = Api(user_gear_api)


class UserGearAPI:

    class _GearCollection(Resource):
        """GET + POST /api/sfi/gear"""
        @token_required()
        def get(self):
            items = UserGear.get_by_user(g.current_user.id)
            return jsonify([item.to_dict() for item in items])

        @token_required()
        def post(self):
            body = request.get_json()
            if not body or not body.get('name', '').strip():
                return {'error': 'name is required'}, 400
            gear = UserGear.create(g.current_user.id, body)
            return jsonify(gear.to_dict())

    class _GearItem(Resource):
        """DELETE /api/sfi/gear/<id>"""
        @token_required()
        def delete(self, gear_id):
            gear = UserGear.query.get(gear_id)
            if not gear:
                return {'error': 'not found'}, 404
            if gear.user_id != g.current_user.id:
                return {'error': 'forbidden'}, 403
            gear.delete()
            return jsonify({'message': 'deleted'})

    api.add_resource(_GearCollection, '/gear')
    api.add_resource(_GearItem, '/gear/<int:gear_id>')
