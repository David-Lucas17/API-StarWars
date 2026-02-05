def sort_results(results, sort_by, order="asc"):
    if not results:
        return []
    
    def get_sort_value(item):
        value = item.get(sort_by)
        
        if isinstance(value, str):
            try:
                if "BBY" in value:
                    return float(value.replace("BBY", "").strip())
                elif "ABY" in value:
                    return float(value.replace("ABY", "").strip())
            except (ValueError, AttributeError):
                pass
        
        return value
    
    reverse = (order.lower() == "desc")
    
    try:
        sorted_results = sorted(
            results, 
            key=lambda x: get_sort_value(x), 
            reverse=reverse
        )
        return sorted_results
    except (TypeError, KeyError):
        return results