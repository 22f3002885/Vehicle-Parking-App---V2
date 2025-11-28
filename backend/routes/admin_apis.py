from flask_restful import Resource, reqparse
from flask_security import roles_required
from flask import jsonify, make_response, request
from models import db, ParkingLot, ParkingSpot, Reservation, User
from sqlalchemy import func

lot_parser = reqparse.RequestParser()
lot_parser.add_argument('name', type=str, required=True)
lot_parser.add_argument('price_per_hour', type=float, required=True)
lot_parser.add_argument('address', type=str, required=True)
lot_parser.add_argument('pincode', type=str, required=True)
lot_parser.add_argument('max_spots', type=int, required=True)

class AdminLotsAPI(Resource):
    @roles_required('admin')
    def get(self):
        lots = ParkingLot.query.all()
        result = []
        for lot in lots:
            total_spots = len(lot.spots)
            occupied_spots = sum(1 for s in lot.spots if s.status == 'O')
            result.append({
                'id': lot.id,
                'name': lot.name,
                'price_per_hour': lot.price_per_hour,
                'address': lot.address,
                'pincode': lot.pincode,
                'max_spots': lot.max_spots
            })
        return make_response(jsonify(result), 200)
    
    @roles_required('admin')
    def post(self):
        args = lot_parser.parse_args()
        name = args['name']
        price_per_hour = args['price_per_hour']
        address = args['address']
        pincode = args['pincode']
        max_spots = args['max_spots']

        new_lot = ParkingLot(
            name=name,
            price_per_hour=price_per_hour,
            address=address,
            pincode=pincode,
            max_spots=max_spots
        )
        db.session.add(new_lot)
        db.session.commit()

        for _ in range(max_spots):
            spot = ParkingSpot(
                lot_id=new_lot.id
            )
            db.session.add(spot)
        
        db.session.commit()

        response = {
            'message': 'Parking lot created successfully.',
            'lot_details': {
                'id': new_lot.id,
                'name': new_lot.name,
                'price_per_hour': new_lot.price_per_hour,
                'address': new_lot.address,
                'pincode': new_lot.pincode,
                'max_spots': new_lot.max_spots
            }
        }
        return make_response(jsonify(response), 201)
    

class AdminLotDetailAPI(Resource):
    @roles_required('admin')
    def delete(self, lot_id):
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return make_response(jsonify({'message': 'Parking lot not found.'}), 404)
        
        if any(spot.status == 'O' for spot in lot.spots):
            return make_response(jsonify({'message': 'Cannot delete lot with occupied spots.'}), 400)
        
        ParkingSpot.query.filter_by(lot_id=lot.id).delete()
        db.session.delete(lot)
        db.session.commit()

        return make_response(jsonify({'message': 'Parking lot deleted successfully.'}), 200)
    
    @roles_required('admin')
    def put(self, lot_id):
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return make_response(jsonify({'message': 'Parking lot not found.'}), 404)
        
        args = lot_parser.parse_args()
        lot.name = args['name']
        lot.price_per_hour = args['price_per_hour']
        lot.address = args['address']
        lot.pincode = args['pincode']
        
        db.session.commit()
        response = {
            'message': 'Parking lot updated successfully.',
            'lot_details': {
                'id': lot.id,
                'name': lot.name,
                'price_per_hour': lot.price_per_hour,
                'address': lot.address,
                'pincode': lot.pincode,
                'max_spots': lot.max_spots
            }
        }
        return make_response(jsonify(response), 200)
    
    @roles_required('admin')
    def get(self, lot_id):
        lot = ParkingLot.query.get(lot_id)
        spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()
        response = {
            "spots": [
                {"id": s.id, "status": s.status}
                for s in spots
            ]
        }
        return make_response(jsonify(response), 200)
    
class AdminSpotDetailAPI(Resource):
    @roles_required('admin')
    def get(self, spot_id):
        spot = ParkingSpot.query.get(spot_id)
        if spot.status == 'O':
            reservation = Reservation.query.filter_by(spot_id=spot.id).first()
            reservation_info = {
                'vehicle_number': reservation.vehicle_number,
                'entry_time': reservation.entry_time,
                'user_id': reservation.user_id
            }
            return make_response(jsonify(reservation_info), 200)
        
        response = {
            'message': 'Spot is available.'
        }
        return make_response(jsonify(response), 200)
    
    @roles_required('admin')
    def delete(self, spot_id):
        spot = ParkingSpot.query.get(spot_id)
        if not spot:
            return make_response(jsonify({'message': 'Parking spot not found.'}), 404)
        
        if spot.status == 'O':
            return make_response(jsonify({'message': 'Cannot delete an occupied spot.'}), 400)
        
        db.session.delete(spot)
        lot = ParkingLot.query.get(spot.lot_id)
        lot.max_spots -= 1
        db.session.commit()

        return make_response(jsonify({'message': 'Parking spot deleted successfully.'}), 200)
    
class AdminUsersAPI(Resource):
    @roles_required('admin')
    def get(self):
        users = User.query.all()
        result = []
        for user in users:
            result.append({
                'id': user.id,
                'email': user.email,
                'roles': [role.name for role in user.roles]
            })
        return make_response(jsonify(result), 200)
    
class AdminReservationsAPI(Resource):
    @roles_required('admin')
    def get(self):
        reservations = Reservation.query.all()
        result = []
        for res in reservations:
            lot = ParkingLot.query.get(res.lot_id)
            result.append({
                'reservation_id': res.id,
                'vehicle_number': res.vehicle_number,
                'entry_time': res.entry_time,
                'exit_time': res.exit_time,
                'total_cost': res.total_cost,
                'lot_name': lot.name,
                'address': res.address,
                'user_id': res.user_id
            })
        return make_response(jsonify(result), 200)
    
class AdminSummaryAPI(Resource):
    @roles_required('admin')
    def get(self):
        total_lots = ParkingLot.query.count()
        total_spots = ParkingSpot.query.count()
        occupied_spots = ParkingSpot.query.filter_by(status='O').count()
        total_users = User.query.count()

        summary = {
            'total_lots': total_lots,
            'total_spots': total_spots,
            'occupied_spots': occupied_spots,
            'total_users': total_users
        }
        return make_response(jsonify(summary), 200)