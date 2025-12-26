from flask import Flask
from flask_cors import CORS
from backend.routes.soal_routes import soal_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(soal_bp, url_prefix="/api/soal")


if __name__ == "__main__":
    app.run(debug=True)
