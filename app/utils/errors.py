class SWAPIError(Exception):
    """Exceção personalizada para erros da SWAPI"""
    pass

class ResourceNotFoundError(Exception):
    """Exceção para recurso não encontrado"""
    pass

class ValidationError(Exception):
    """Exceção para erros de validação"""
    pass