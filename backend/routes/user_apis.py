from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import roles_required, current_user
from models import db, ParkingLot, ParkingSpot, Reservation
from sqlalchemy import func, desc
from datetime import datetime, timedelta

class CurrentUserReservationsAPI(Resource):
    @roles_required('user')
    def get(self):
        user_id = current_user.id
        active_reservations = Reservation.query.filter_by(user_id=user_id, exit_time=None).all()
        result = []
        for res in active_reservations:
            spot = ParkingSpot.query.get(res.spot_id)
            lot = ParkingLot.query.get(res.lot_id)
            result.append({
                'reservation_id': res.id,
                'vehicle_number': res.vehicle_number,
                'entry_time': res.entry_time,
                'lot_name': lot.name,
                'spot_id': spot.id,
                'address': res.address
            })
        
        return make_response(jsonify({'active_reservations': result}), 200)

class UserParkinglotsListAPI(Resource):
    @roles_required('user')
    def get(self):
        lots = ParkingLot.query.all()
        result = []
        for lot in lots:
            available_spots = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').count()
            result.append({
                'lot_id': lot.id,
                'name': lot.name,
                'address': lot.address,
                'price_per_hour': lot.price_per_hour,
                'available_spots': available_spots
            })
        return make_response(jsonify({'parking_lots': result}), 200)

class UserParkinglotDetailAPI(Resource):
    @roles_required('user')
    def get(self, lot_id):
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return make_response(jsonify({'message': 'Parking lot not found.'}), 404)
        
        available_spots = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').count()
        lot_info = {
            'lot_id': lot.id,
            'name': lot.name,
            'address': lot.address,
            'price_per_hour': lot.price_per_hour,
            'available_spots': available_spots
        }
        return make_response(jsonify({'lot': lot_info}), 200)

    
class UserHistoryAPI(Resource):
    @roles_required('user')
    def get(self):
        user_id = current_user.id
        past_reservations = Reservation.query.filter(Reservation.user_id==user_id, Reservation.exit_time!=None).order_by(desc(Reservation.exit_time)).all()
        result = []
        for res in past_reservations:
            lot = ParkingLot.query.get(res.lot_id)
            result.append({
                'reservation_id': res.id,
                'vehicle_number': res.vehicle_number,
                'entry_time': res.entry_time,
                'exit_time': res.exit_time,
                'total_cost': res.total_cost,
                'lot_name': lot.name,
                'address': res.address
            })
        
        return make_response(jsonify({'past_reservations': result}), 200)
    

class UserReserveSpotAPI(Resource):
    @roles_required('user')
    def post(self, lot_id):
        data = request.get_json()
        vehicle_number = data.get('vehicle_number')

        spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
        if not spot:
            return make_response(jsonify({'message': 'No available spots in this lot.'}), 404)
        
        spot.status = 'O'
        reservation = Reservation(
            vehicle_number=vehicle_number,
            entry_time=datetime.now(),
            user_id=current_user.id,
            spot_id=spot.id,
            lot_id=lot_id,
            address=ParkingLot.query.get(lot_id).address
        )
        db.session.add(reservation)
        db.session.commit()

        response = {
            'message': 'Spot reserved successfully.',
            'reservation_details': {
                'reservation_id': reservation.id,
                'spot_id': spot.id,
                'entry_time': reservation.entry_time,
                'vehicle_number': reservation.vehicle_number,
                'address': reservation.address
            }
        }
        return make_response(jsonify(response), 201)
    
class UserReleaseSpotAPI(Resource):
    @roles_required('user')
    def post(self, reservation_id):
        reservation = Reservation.query.get(reservation_id)
        if not reservation:
            return make_response(jsonify({'message': 'Reservation not found.'}), 404)
        
        if reservation.exit_time is not None:
            return make_response(jsonify({'message': 'Spot already released.'}), 400)
        
        spot = ParkingSpot.query.get(reservation.spot_id)
        spot.status = 'A'
        reservation.exit_time = datetime.now()
        duration = (reservation.exit_time - reservation.entry_time).total_seconds() / 3600
        lot = ParkingLot.query.get(reservation.lot_id)
        reservation.total_cost = round(duration * lot.price_per_hour, 2)

        db.session.commit()

        response = {
            'message': 'Spot released successfully.',
            'reservation_summary': {
                'reservation_id': reservation.id,
                'user_id': reservation.user_id,
                'vehicle_number': reservation.vehicle_number,
                'entry_time': reservation.entry_time,
                'exit_time': reservation.exit_time,
                'total_cost': reservation.total_cost
            }
        }
        return make_response(jsonify(response), 200)

class UserSpotStatusSummaryAPI(Resource):
    @roles_required('user')
    def get(self):
        released_count = ParkingSpot.query.filter_by(status='A').count()
        occupied_count = ParkingSpot.query.filter_by(status='O').count()
        return make_response(jsonify({'released': released_count, 'occupied': occupied_count}), 200)