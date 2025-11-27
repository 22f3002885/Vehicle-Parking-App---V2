from database import db
from flask_security import UserMixin, RoleMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)

    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    fs_token_uniquifier = db.Column(db.String(255), unique=True, nullable=True)

    roles = db.relationship('Role', secondary='user_roles')
    reservations = db.relationship('Reservation', backref='user', lazy=True)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

class ParkingLot(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable = False)
    price_per_hour = db.Column(db.Float, nullable = False)
    address = db.Column(db.String(128), nullable = False)
    pincode = db.Column(db.String(16), nullable = False)
    max_spots = db.Column(db.Integer, nullable = False)
    
    spots = db.relationship('ParkingSpot', backref='lot', lazy=True)

class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    status = db.Column(db.String(1), default='A', nullable=False) 
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable = False)

    reservations = db.relationship('Reservation', backref='spot', lazy=True)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    vehicle_number = db.Column(db.String(16), unique = False, nullable = False)
    entry_time = db.Column(db.DateTime, nullable = False)
    exit_time = db.Column(db.DateTime) 
    total_cost = db.Column(db.Float) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable = False)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable = False)
    address = db.Column(db.String(128), nullable = False)