from flask import Flask
from config import Config
from models import db
from datastore import user_datastore
from flask_security import Security
from routes import main_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    security = Security(app, user_datastore)
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()
        # Optional: Initialize admin/role like in previous examples

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
