from app import create_app
from endpoints import api_bp

app = create_app()
app.register_blueprint(api_bp)
