from flask import Flask
from bson.objectid import ObjectId
from pymongo import MongoClient
from flask_login import LoginManager

client=MongoClient('mongodb://127.0.0.1:27017/')
db = client.testinglogin
login_manager = LoginManager()
def create_app():
	
	app=Flask(__name__)
	app.secret_key='somesecret'
	
	
	login_manager.login_view= 'auth.login'
	login_manager.init_app(app)
	#print('')

	from .models import User

	@login_manager.user_loader
	def user_loader(_id):
		print('---->',_id)
		check = db.users.find_one({"_id":ObjectId(_id)})
		print(check)
		print('here in loader')
		if not check:
			return

		user = User(check['_id'])
		#user.id = email
		return user

	@login_manager.request_loader
	def request_loader(request):
		email = request.form.get('email')
		#if email not in users:
		#	return
		check = db.users.find_one({"email":email})
		if not check:
			return

		user = User(check['_id'])
		#user.id = email

		user.is_authenticated = User.validate_login(check['password'],request.form['password'])
		return user

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	return app



