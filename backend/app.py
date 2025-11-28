from flask import Flask
from flask_security import Security
from flask_restful import Api, Resource
from database import db
from config import Config
from user_datastore import user_datastore

from werkzeug.security import generate_password_hash
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    security = Security(app, user_datastore)

    api = Api(app)

    with app.app_context():
        db.create_all()

        admin_role = user_datastore.find_or_create_role(name='admin', description='Administrator')
        user_role = user_datastore.find_or_create_role(name='user', description='End user')

        if not user_datastore.find_user(email='admin@gmail.com'):
            user_datastore.create_user(email='admin@gmail.com', password=generate_password_hash('admin'), roles=[admin_role])

        db.session.commit()

    return app, api

app, api = create_app()
CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5000"])

app.route('/')
def index():
    return {
        'message': "Welcome to the Vehicle Parking App API"
    }, 200

from routes.auth_apis import LoginAPI, LogoutAPI, RegisterAPI

api.add_resource(LoginAPI, '/api/login')
api.add_resource(LogoutAPI, '/api/logout')
api.add_resource(RegisterAPI, '/api/register')

from routes.admin_apis import AdminLotsAPI, AdminLotDetailAPI, AdminSpotDetailAPI, AdminUsersAPI, AdminReservationsAPI, AdminSummaryAPI

api.add_resource(AdminLotsAPI, '/api/admin/lots')
api.add_resource(AdminLotDetailAPI, '/api/admin/lots/<int:lot_id>')
api.add_resource(AdminSpotDetailAPI, '/api/admin/spots/<int:spot_id>')
api.add_resource(AdminUsersAPI, '/api/admin/users')
api.add_resource(AdminReservationsAPI, '/api/admin/reservations')
api.add_resource(AdminSummaryAPI, '/api/admin/summary')

from routes.user_apis import CurrentUserReservationsAPI, UserParkinglotsAPI, UserHistoryAPI, UserReserveSpotAPI, UserReleaseSpotAPI, UserSummaryAPI

api.add_resource(CurrentUserReservationsAPI, '/api/user/dashboard')
api.add_resource(UserParkinglotsAPI, '/api/user/parkinglots')
api.add_resource(UserHistoryAPI, '/api/user/history')
api.add_resource(UserReserveSpotAPI, '/api/user/reserve/<int:lot_id>')
api.add_resource(UserReleaseSpotAPI, '/api/user/release/<int:reservation_id>')
api.add_resource(UserSummaryAPI, '/api/user/summary')

if __name__ == "__main__":
    app.run(debug=True)