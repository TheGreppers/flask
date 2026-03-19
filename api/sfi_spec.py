"""
SFI Spec Search API — search and browse SFI Foundation specifications.

Endpoints:
    GET /api/sfi/specs          — list all specs (with optional filters)
    GET /api/sfi/specs/search   — keyword search across product names,
                                  spec numbers, and categories
"""

from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from model.sfi_spec import SfiSpec

sfi_spec_api = Blueprint('sfi_spec_api', __name__, url_prefix='/api/sfi')
api = Api(sfi_spec_api)


class SfiSpecAPI:
    """API resources for SFI spec search and retrieval."""

    class _Search(Resource):
        """GET /api/sfi/specs/search?q=<keyword>

        Searches product_name, spec_number, category, and subcategory.
        Returns matching specs as a JSON array.
        """
        def get(self):
            query = request.args.get('q', '').strip()
            if not query:
                return {"error": "Missing 'q' query parameter"}, 400

            keyword = f"%{query}%"
            results = SfiSpec.query.filter(
                (SfiSpec.product_name.ilike(keyword)) |
                (SfiSpec.spec_number.ilike(keyword)) |
                (SfiSpec.category.ilike(keyword)) |
                (SfiSpec.subcategory.ilike(keyword))
            ).all()

            return jsonify([spec.to_dict() for spec in results])

    class _List(Resource):
        """GET /api/sfi/specs?category=<name>

        Returns all specs, optionally filtered by category.
        """
        def get(self):
            category = request.args.get('category', '').strip()
            if category:
                results = SfiSpec.query.filter(
                    SfiSpec.category.ilike(f"%{category}%")
                ).all()
            else:
                results = SfiSpec.query.all()

            return jsonify([spec.to_dict() for spec in results])

    class _Categories(Resource):
        """GET /api/sfi/categories

        Returns the list of distinct categories.
        """
        def get(self):
            rows = SfiSpec.query.with_entities(
                SfiSpec.category
            ).distinct().all()
            return jsonify([row.category for row in rows])

    # Register routes
    api.add_resource(_Search, '/specs/search')
    api.add_resource(_List, '/specs')
    api.add_resource(_Categories, '/categories')
