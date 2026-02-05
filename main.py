from flask import Flask
from app.routes import api_bp
import functions_framework

app = Flask(__name__)
app.register_blueprint(api_bp)

@functions_framework.http
def main(request):
    return app
