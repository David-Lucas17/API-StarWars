"""
Ponto de entrada para Google Cloud Functions.
"""
from app.main import app
import functions_framework

@functions_framework.http
def starwars_api(request):
    return app(request)