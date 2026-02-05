def filter_by_field(results, field, value):
    if not results:
        return []
    
    filtered = []
    for item in results:
        field_value = get_nested_field(item, field)
        if str(field_value).lower() == str(value).lower():
            filtered.append(item)
    
    return filtered

def get_nested_field(item, field_path):
    """
    Obtém um campo aninhado de um dicionário
    """
    keys = field_path.split('.')
    value = item
    
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key)
        else:
            return None
    
    return value