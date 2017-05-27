from flask import render_template, request, redirect, session
from Project import app, db, login_manager
from Project.models import User, Ride_Request, Ride_Offer
from flask_login import login_user, login_required, logout_user, current_user



@app.route('/', methods = ['GET'])
def start():
	return render_template('index.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')


@app.route('/services')
def services():
	return render_template('services.html')


@app.route('/map')
def map():
	return render_template('map.html')

@app.route('/display_registration')
def display_registration():
	return render_template('register.html')


@app.route('/register', methods = ['POST'])
def driver_insert():
	name = request.form["firstName"]
	last = request.form["lastName"]
	phone = request.form["phonenumber"]
	email = request.form["email"]
	user = request.form["username"]
	password = request.form["password"]
	fullname = name + " " + last

	newUser = User(username = user, email = email, name = fullname, password = password, phone_number = phone)
	db.session.add(newUser)
	db.session.commit()

	return render_template('login.html')


@app.route('/contact_us', methods = ['POST'])
def contact_us():

	return render_template('thankContact.html')

@app.route('/display_login')
def display_login():
	return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    user_name = request.form['username']
    user = db.session.query(User).filter_by(username = user_name).first()
    if request.form['password'] == user.password:
        login_user(user)
        return redirect("/")
    return 'Bad login'


@login_manager.user_loader
def user_loader(user_id):
	for instance in db.session.query(User).order_by(User.id):
		if instance.get_id() == user_id:
			return instance



@app.route('/ride_request')
@login_required
def display_ride_request():
	return render_template('requests.html')


@app.route('/post_request', methods = ['POST'])
@login_required
def ride_request_insert():
	pickUp = request.form["pickUp"]
	dropOff = request.form["dropOff"]
	time = request.form["time"]
	date = request.form["date"]

	newRequest = Ride_Request(pickup= pickUp, location = dropOff, ride_date = date, time = time, from_user = current_user.username)
	db.session.add(newRequest)
	db.session.commit()
	#context = {'requests':Ride_Request.query.all()}
	return redirect('/view_requests')#, **context)


@app.route('/request_success')
@login_required
def request_success():
	return render_template('ridesuccess.htm')


@app.route('/ride_offer')
@login_required
def display_ride_offer():
	return render_template('offers.html')


@app.route('/post_offer', methods = ['POST'])
@login_required
def ride_offer_insert():
	pickUp = request.form["pickUp"]
	dropOff = request.form["dropOff"]
	time = request.form["time"]
	date = request.form["date"]
	NumPas = request.form["Pas"]

	newOffer = Ride_Offer(date, dropOff, pickUp, int(NumPas), time, current_user.username)
	db.session.add(newOffer)
	db.session.commit()
	#context = {'requests':Ride_Offer.query.all()}
	return redirect('/view_offers') #, **context)


@app.route('/view_requests')
@login_required
def display_requests(): 
	#Query so only non-accpeted, not current_user issued are shown
	context = {'requests':db.session.query(Ride_Request).filter(Ride_Request.is_Accepted == 0, Ride_Request.from_user != current_user.username)}
	return render_template('rides_table.html', **context)


@app.route('/view_offers')
@login_required
def display_offers(): 
	#Query so only non-accpeted, not current_user issued are shown
	context = {'requests':db.session.query(Ride_Offer).filter(Ride_Offer.is_Accepted == 0, Ride_Offer.from_user != current_user.username)}
	return render_template('offers_table.html', **context)


@app.route('/accept_request/<int:request_id>', methods=['POST'])
@login_required
def accept_request(request_id):
	my_Request = db.session.query(Ride_Request).get(request_id)
	my_Request.is_Accepted = 1
	my_Request.id_Acceptor = current_user.id
	db.session.add(my_Request)
	db.session.commit()
	return redirect("/view_requests")


@app.route('/accept_offer/<int:offer_id>', methods= ['POST'])
@login_required
def accept_offer(offer_id):
	my_Offer= db.session.query(Ride_Offer).get(offer_id)
	my_Offer.is_Accepted = 1
	my_Offer.id_Acceptor = current_user.id
	db.session.add(my_Offer)
	db.session.commit()
	return redirect("/view_offers")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/my_profile")
@login_required
def myprof():
	return render_template("dashboard.html")



@app.route("/bookings")
@login_required
def show_accepted_rides():
	contact_list = []

	my_accepted_offers = db.session.query(Ride_Offer).filter(Ride_Offer.from_user == current_user.username, Ride_Offer.is_Accepted == 1)

	offers_I_accepted = db.session.query(Ride_Offer).filter(Ride_Offer.id_Acceptor == current_user.id, Ride_Offer.is_Accepted == 1)

	my_accepted_requests = db.session.query(Ride_Request).filter(Ride_Request.from_user == current_user.username, Ride_Request.is_Accepted == 1)

	requests_I_accepted = db.session.query(Ride_Request).filter(Ride_Request.id_Acceptor == current_user.id, Ride_Request.is_Accepted == 1)

	context = {"my_accepted_offers":my_accepted_offers, "my_accepted_requests": my_accepted_requests, "offers_I_accepted": offers_I_accepted, "requests_I_accepted": requests_I_accepted, "contacts": User.query.all()}
	return render_template("bookings.html", **context)


@app.route("/listridesoffer")
@login_required
def display_my_offers():
	context = {"offers": db.session.query(Ride_Offer).filter(Ride_Offer.from_user == current_user.username, Ride_Offer.is_Accepted == 0)}
	return render_template("listridesoffer.html", **context)


@app.route("/unaccepted_rides")
@login_required
def display_my_requests():
	context = {"requests": db.session.query(Ride_Request).filter(Ride_Request.from_user == current_user.username, Ride_Request.is_Accepted == 0)}
	return render_template("unaccepted_rides.html", **context)




@app.route('/delete_request/<int:request_id>', methods=['POST'])
@login_required
def delete_request(request_id):
	my_Request = db.session.query(Ride_Request).get(request_id)
	db.session.delete(my_Request)
	db.session.commit()
	return redirect("/bookings")



@app.route('/delete_/<int:request_id>', methods=['POST'])
@login_required
def delete_(request_id):
	my_Request = db.session.query(Ride_Request).get(request_id)
	db.session.delete(my_Request)
	db.session.commit()
	return redirect("/unaccepted_rides")



@app.route('/delete_offer/<int:offer_id>', methods=['POST'])
@login_required
def delete_offer(offer_id):
	my_Request = db.session.query(Ride_Offer).get(offer_id)
	db.session.delete(my_Request)
	db.session.commit()
	return redirect("/bookings")
