from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import date,datetime
import os
from flask_cors import CORS
# init app
app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
# DataBase
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACKER_MODIFICATION'] = False

# init db
db = SQLAlchemy(app)

# init ma
ma = Marshmallow(app)


# Product class/model
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100),nullable=False)
    vehicle_id = db.Column(db.String(200),nullable=False)
    start_date = db.Column(db.DateTime,nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    pickup_location = db.Column(db.String,nullable=False)
    vehicle_imagePath = db.Column(db.String,nullable=False)
    vehicle_name = db.Column(db.String,nullable=False)
    return_location = db.Column(db.String, nullable=False)
    is_payment_online=db.Column(db.Boolean,nullable=False)
    total_price=db.Column(db.Float,nullable=False)

    def __init__(self, user_id, vehicle_id, start_date,end_date,total_price,pickup_location,return_location,is_payment_online , vehicle_name , vehicle_imagePath):
        self.user_id=user_id
        self.vehicle_id=vehicle_id
        self.start_date=start_date
        self.end_date=end_date
        self.total_price = total_price
        self.pickup_location = pickup_location
        self.return_location = return_location
        self.is_payment_online=is_payment_online
        self.vehicle_name=vehicle_name
        self.vehicle_imagePath=vehicle_imagePath

db.create_all()
db.session.commit()
# product schema
class BookingSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'vehicle_id', 'start_date', 'end_date','total_price','pickup_location','return_location','is_payment_online' , 'vehicle_name' , 'vehicle_imagePath')


# init schema
booking_schema= BookingSchema()
booking_schema = BookingSchema(many=True)


# create Product
@app.route('/addBooking', methods=['POST'])
def add_product():
    keys=['user_id','vehicle_id','start_date','end_date','total_price','is_payment_online','pickup_location','return_location' , 'vehicle_name' , 'vehicle_imagePath']
    for key in keys:
        if not request.args.get(key):
            return jsonify({'Error ': 'All fields are required'})

    user_id = request.args.get('user_id')
    vehicle_id = request.args.get('vehicle_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    total_price = request.args.get('total_price')
    pickup_location = request.args.get('pickup_location')
    is_payment_online = bool(request.args.get('is_payment_online'))
    vehicle_name = request.args.get('vehicle_name')
    vehicle_imagePath = request.args.get('vehicle_imagePath')
    return_location=request.args.get('return_location')
    start_date=datetime.strptime(start_date, '%Y-%m-%d')
    end_date=datetime.strptime(end_date, '%Y-%m-%d')
    new_booking = Booking(user_id=user_id, vehicle_id=vehicle_id, start_date=start_date,end_date=end_date,total_price=total_price,pickup_location=pickup_location,return_location=return_location,is_payment_online=is_payment_online , vehicle_name=vehicle_name , vehicle_imagePath=vehicle_imagePath)

    db.session.add(new_booking)
    db.session.commit()

    return jsonify({"message":"new booking have been added",
                    "data":{
                        "user_id":new_booking.user_id,
                        "vehicle_id":new_booking.vehicle_id,
                        "start_date":new_booking.start_date,
                        "end_date":new_booking.end_date,
                        "total_price": new_booking.total_price,
                        "pickup_location": pickup_location,
                        "return_location": return_location,
                        'is_payment_online':new_booking.is_payment_online,
                        'vehicle_name':new_booking.vehicle_name,
                        'vehicle_imagePath':new_booking.vehicle_imagePath
                    }
                    })

@app.route("/",methods=['GET'])
def get_products():
    all_bookings=[]
    bookings=Booking.query.all()
    for b in bookings:
        booking={}
        booking['id']=b.id
        booking['user_id']=b.user_id
        booking['vehicle_id']=b.vehicle_id
        booking['start_date']=b.start_date
        booking['end_date']=b.end_date
        booking['total_price'] = b.total_price
        booking['pickup_location'] = b.pickup_location
        booking['return_location'] = b.return_location
        booking['is_payment_online'] = b.is_payment_online,
        booking['vehicle_name'] = b.vehicle_name,
        booking['vehicle_imagePath'] = b.vehicle_imagePath
        all_bookings.append(booking)

    return jsonify({
        "data":all_bookings
    })


@app.route("/deleteBooking",methods=['POST'])
def deleteBooking():
    if not request.args.get('id'):
        return  jsonify({"error":"id is required"})
    id=request.args.get('id')
    if Booking.query.filter_by(id=id).delete()>0:
        db.session.commit()
        return jsonify({"message": "record deleted"})
    else:
        return jsonify({"error": "no record found with id {}".format(id)})
@app.route('/getBooking', methods=['GET'])
def getBooking():
    if request.args.get('user_id'):
        all_bookings=[]
        id = request.args.get('user_id')
        query = Booking.query.filter_by(user_id=id)
        result = query.all()
        for b in result:
            booking={}
            booking['id']=b.id
            booking['user_id']=b.user_id
            booking['vehicle_id']=b.vehicle_id
            booking['start_date']=b.start_date
            booking['end_date']=b.end_date
            booking['total_price'] = b.total_price
            booking['pickup_location'] = b.pickup_location
            booking['return_location'] = b.return_location
            booking['is_payment_online']=b.is_payment_online
            booking['vehicle_name']=b.vehicle_name
            booking['vehicle_imagePath']=b.vehicle_imagePath
            all_bookings.append(booking)

        return jsonify({
            "data":all_bookings
        })


@app.route('/getOneBooking', methods=['GET'])
def getOneBooking():
    if request.args.get('id'):
        all_bookings=[]
        id = request.args.get('id')
        query = Booking.query.filter_by(id=id)
        result = query.all()
        for b in result:
            booking={}
            booking['id']=b.id
            booking['user_id']=b.user_id
            booking['vehicle_id']=b.vehicle_id
            booking['start_date']=b.start_date
            booking['end_date']=b.end_date
            booking['total_price'] = b.total_price
            booking['pickup_location'] = b.pickup_location
            booking['return_location'] = b.return_location
            booking['is_payment_online']=b.is_payment_online
            booking['vehicle_name']=b.vehicle_name
            booking['vehicle_imagePath']=b.vehicle_imagePath
            all_bookings.append(booking)

        return jsonify({
            "data":all_bookings
        })



@app.route("/updateBooking",methods=['POST'])
def updateBooking():
    booking_record = {}
    id=request.args.get('id')
    booking_record['user_id'] = request.args.get('user_id')
    booking_record['vehicle_id'] = request.args.get('vehicle_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    booking_record['total_price'] = request.args.get('total_price')
    booking_record['pickup_location'] = request.args.get('pickup_location')
    booking_record['return_location'] = request.args.get('return_location')
    booking_record['vehicle_name'] = request.args.get('vehicle_name')
    booking_record['vehicle_imagePath'] = request.args.get('vehicle_imagePath')
    booking_record['is_payment_online']=bool(request.args.get('is_payment_online'))
    booking_record['start_date']=datetime.strptime(start_date, '%Y-%m-%d')
    booking_record['end_date']=datetime.strptime(end_date, '%Y-%m-%d')

    if Booking.query.filter_by(id=id).update(booking_record)>0:
        db.session.commit()
        return jsonify({'message':'record have been updated'})
    else:
        return jsonify({'error':'error while updating record'})
    # db.session.add(new_booking)
    # db.session.commit()
    #
    # return jsonify({"message":"new booking have been added",
    #                 "data":{
    #                     "user_id":new_booking.user_id,
    #                     "vehicle_id":new_booking.vehicle_id,
    #                     "start_date":new_booking.start_date,
    #                     "end_date":new_booking.end_date,
    #                     "total_price":new_booking.total_price
    #                 }
    #                 })

if __name__ == '__main__':
    app.run()
