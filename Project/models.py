from Project import db

user_to_request = db.Table('request_association', db.Model.metadata, db.Column('User_id', db.Integer, db.ForeignKey('user.id')), db.Column('Ride_Request_id', db.Integer, db.ForeignKey('ride_requests.id')))
user_to_offer = db.Table('offer_association', db.Model.metadata, db.Column('User_id', db.Integer, db.ForeignKey('user.id')), db.Column('Ride_Offer_id', db.Integer, db.ForeignKey('ride_offers.id')))

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(200))
    name = db.Column(db.String(200))
    phone_number = db.Column(db.Integer)
    password = db.Column(db.String(200))
    email = db.Column(db.String(200))
    requests = db.relationship("Ride_Request", secondary=user_to_request, backref=db.backref('user', lazy='dynamic'))
    offers = db.relationship("Ride_Offer", secondary=user_to_offer, backref=db.backref('user', lazy='dynamic'))
   
    #my_requests = db.relationship("Ride_Request", back_populates = "requester")
    #Ride_Offer_Relation = db.relationship('Ride_Offer', secondary = 'rider_to_offer', back_populates = "Riders_Relation")

    def __init__(self, phone_number, password, email, name, username):
        self.phone_number = phone_number
        self.password = password
        self.email = email
        self.name = name
        self.username = username
        self.password = password #bcrypt.generate_password_hash(password)

    def is_authenticated(self):
        if self == current_user:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)




class Ride_Request(db.Model):
    __tablename__ = 'ride_requests'
    id = db.Column(db.Integer, primary_key = True)
    ride_date = db.Column(db.String(200))
    location = db.Column(db.String(200))
    pickup = db.Column(db.String(200))
    time = db.Column(db.String(200))
    from_user = db.Column(db.String(200))
    id_Acceptor = db.Column(db.Integer, default = 0)
    is_Accepted = db.Column(db.Integer, default = 0)
    users = db.relationship("User", secondary=user_to_request, backref=db.backref('ride_requests', lazy='dynamic'))


    #Requester_id = db.Column(db.String(200), db.ForeignKey('riders.id'))
    #requester = db.relationship("Rider", back_populates = "my_requests")
    #Driver_id = db.Column(db.String(200), db.ForeignKey('drivers.id'))
    #driver = db.relationship("Driver", back_populates = "myride_requests")

    def __init__(self, ride_date, location, pickup, time, from_user):
        self.ride_date = ride_date
        self.location = location
        self.pickup = pickup
        self.time = time
        self.from_user = from_user
        

class Ride_Offer(db.Model):
    __tablename__ = 'ride_offers'
    id = db.Column(db.Integer, primary_key = True)
    ride_date = db.Column(db.String(200))
    location = db.Column(db.String(200))
    num_passengers = db.Column(db.Integer)
    pickup = db.Column(db.String(200))
    time = db.Column(db.String(200))
    from_user = db.Column(db.String(200))
    id_Acceptor = db.Column(db.Integer, default = 0)
    is_Accepted = db.Column(db.Integer, default = 0)
    users = db.relationship("User", secondary=user_to_offer, backref=db.backref('ride_offers', lazy='dynamic'))
    #Driver_id = db.Column(db.String(200), db.ForeignKey('drivers.id'))
    #driver = db.relationship("Driver", back_populates = "myride_offers")
    #Riders_Relation = db.relationship('Rider', secondary = 'rider_to_offer', back_populates = "Ride_Offer_Relation")

    def __init__(self, ride_date, location, pickup, num_passengers, time, from_user):
        self.ride_date = ride_date
        self.num_passengers = num_passengers
        self.location = location
        self.pickup = pickup
        self.time = time
        self.from_user = from_user

 

class Reviews(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key = True)
    Agg = db.Column(db.Integer)
    #Driver_Parent_Id = db.Column(db.String(200), db.ForeignKey('drivers.id'))
    #driver = db.relationship("Driver", back_populates = 'driver_reviews')

    def __init__(self, Agg):
        self.Agg = Agg
