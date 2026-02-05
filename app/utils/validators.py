VALID_RESOURCES = ["people", "planets", "films", "species", "vehicles", "starships"]
VALID_SORT_ORDERS = ["asc", "desc"]

def validate_resource(resource):
    """Valida se o recurso é suportado pela SWAPI"""
    if resource not in VALID_RESOURCES:
        raise ValueError(f"Invalid resource type. Must be one of: {VALID_RESOURCES}")
    return True

def validate_sort_order(order):
    """Valida a direção da ordenação"""
    if order and order not in VALID_SORT_ORDERS:
        raise ValueError(f"Invalid sort order. Must be 'asc' or 'desc'")
    return True

def validate_pagination_params(page, per_page):
    """Valida parâmetros de paginação"""
    if page < 1:
        raise ValueError("Page must be greater than 0")
    if per_page < 1 or per_page > 100:
        raise ValueError("Per page must be between 1 and 100")
    return True