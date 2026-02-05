from flask import Blueprint, request, jsonify
from datetime import datetime
import requests

from app.services.swapi_service import fetch_all_data, fetch_film_characters
from app.utils.filters import filter_by_field
from app.utils.sort import sort_results
from app.utils.validators import validate_resource, validate_sort_order, validate_pagination_params
from app.utils.errors import ValidationError

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request", "message": str(error)}), 400

@api_bp.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@api_bp.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

@api_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "Star Wars API",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@api_bp.route("/starwars/search", methods=["GET"])
def search():
    try:
        resource = request.args.get("type")
        name = request.args.get("name")
        filter_field = request.args.get("filter_field")
        filter_value = request.args.get("filter_value")
        sort_by = request.args.get("sort")
        order = request.args.get("order", "asc")
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        if not resource:
            return jsonify({"error": "Parameter 'type' is required"}), 400
        
        validate_resource(resource)
        validate_sort_order(order)
        validate_pagination_params(page, per_page)

        all_results = fetch_all_data(resource, name)
        
        if filter_field and filter_value:
            all_results = filter_by_field(all_results, filter_field, filter_value)
        
        if sort_by:
            all_results = sort_results(all_results, sort_by, order)
        
        total = len(all_results)
        start = (page - 1) * per_page
        end = start + per_page
        paginated_results = all_results[start:end]
        
        return jsonify({
            "data": paginated_results,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "total_pages": (total + per_page - 1) // per_page if total > 0 else 0
            },
            "filters_applied": {
                "resource": resource,
                "name_search": name,
                "field_filter": f"{filter_field}={filter_value}" if filter_field and filter_value else None
            }
        })
        
    except ValueError as e:
        return jsonify({"error": "Validation error", "message": str(e)}), 400
    except requests.exceptions.RequestException:
        return jsonify({"error": "Failed to fetch data from Star Wars API"}), 502
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@api_bp.route("/starwars/films/<int:film_id>/characters", methods=["GET"])
def get_film_characters(film_id):
    try:
        characters = fetch_film_characters(film_id)
        
        return jsonify({
            "film_id": film_id,
            "count": len(characters),
            "characters": characters
        })
        
    except ValueError as e:
        return jsonify({"error": "Not found", "message": str(e)}), 404
    except requests.exceptions.RequestException:
        return jsonify({"error": "Failed to fetch data from Star Wars API"}), 502
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@api_bp.route("/starwars/resources", methods=["GET"])
def list_resources():
    resources = [
        {"name": "people", "description": "Characters from Star Wars"},
        {"name": "planets", "description": "Planets in the Star Wars universe"},
        {"name": "films", "description": "Star Wars movies"},
        {"name": "species", "description": "Species in Star Wars"},
        {"name": "vehicles", "description": "Vehicles in Star Wars"},
        {"name": "starships", "description": "Starships in Star Wars"}
    ]
    
    return jsonify({
        "resources": resources,
        "count": len(resources)
    })