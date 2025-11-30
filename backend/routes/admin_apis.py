from flask_restful import Resource, reqparse
from flask_security import roles_required
from flask import jsonify, make_response, request
from models import db, ParkingLot, ParkingSpot, Reservation, User
from sqlalchemy import case, func
from cache import cache  # Import from cache.py instead of app.py

lot_parser = reqparse.RequestParser()
lot_parser.add_argument('name', type=str, required=True)
lot_parser.add_argument('price_per_hour', type=float, required=True)
lot_parser.add_argument('address', type=str, required=True)
lot_parser.add_argument('pincode', type=str, required=True)
lot_parser.add_argument('max_spots', type=int, required=True)


class AdminLotsAPI(Resource):
    @roles_required('admin')
    def get(self):
        # Cache parking lots
        lots = cache.get('parking_lots_all')
        
        if lots is None:
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
            cache.set('parking_lots_all', result, timeout=600)
            lots = result
        
        return make_response(jsonify(lots), 200)
    
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

        # Invalidate cache
        cache.delete('parking_lots_all')

        response = {
            'message': 'Parking lot created successfully!',
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

        # Invalidate cache
        cache.delete('parking_lots_all')
        cache.delete(f'parking_lot_{lot_id}')

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

        # Invalidate cache
        cache.delete('parking_lots_all')
        cache.delete(f'parking_lot_{lot_id}')

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
        # Cache individual lot
        cache_key = f'parking_lot_{lot_id}'
        lot_data = cache.get(cache_key)
        
        if lot_data is None:
            lot = ParkingLot.query.get_or_404(lot_id)
            spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()
            lot_data = {
                "lot": {
                    "id": lot.id,
                    "name": lot.name,
                    "price_per_hour": float(lot.price_per_hour),
                    "address": lot.address,
                    "pincode": lot.pincode,
                    "max_spots": lot.max_spots
                },
                "spots": [
                    {"id": s.id, "status": s.status}
                    for s in spots
                ]
            }
            cache.set(cache_key, lot_data, timeout=600)
        
        return make_response(jsonify(lot_data), 200)

    
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

        # Invalidate parking lot cache
        cache.delete('parking_lots_all')
        cache.delete(f'parking_lot_{lot.id}')

        return make_response(jsonify({'message': 'Parking spot deleted successfully.'}), 200)

    
class AdminUsersAPI(Resource):
    @roles_required('admin')
    def get(self):
        users = User.query.all()
        non_admin_users = [
            user for user in users 
            if not any(role.name == 'admin' for role in user.roles)
        ]
        result = []
        for user in non_admin_users:
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

    
class AdminSummaryRevenueAPI(Resource):
    @roles_required('admin')
    def get(self):
        revenue_data = (
            db.session.query(
                ParkingLot.id,
                ParkingLot.name,
                func.coalesce(func.sum(Reservation.total_cost), 0).label('total_revenue')
            )
            .outerjoin(ParkingLot.spots)
            .outerjoin(ParkingSpot.reservations)
            .group_by(ParkingLot.id, ParkingLot.name)
            .all()
        )
        
        result = []
        for lot_id, name, total_revenue in revenue_data:
            result.append({
                'id': lot_id,
                'name': name,
                'total_revenue': float(total_revenue)
            })
        return make_response(jsonify(result), 200)


class AdminSummarySpotsAPI(Resource):
    @roles_required('admin')
    def get(self):
        spot_data = (
            db.session.query(
                ParkingLot.id,
                ParkingLot.name,
                func.count(ParkingSpot.id).label('total_spots'),
                func.sum(case((ParkingSpot.status == 'A', 1), else_=0)).label('available_spots'),
                func.sum(case((ParkingSpot.status == 'O', 1), else_=0)).label('occupied_spots')
            )
            .join(ParkingLot.spots)
            .group_by(ParkingLot.id, ParkingLot.name)
            .all()
        )
        
        result = []
        for lot_id, name, total_spots, available_spots, occupied_spots in spot_data:
            result.append({
                'id': lot_id,
                'name': name,
                'total_spots': int(total_spots),
                'available_spots': int(available_spots),
                'occupied_spots': int(occupied_spots)
            })
        return make_response(jsonify(result), 200)
