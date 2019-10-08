from werkzeug.security import check_password_hash
from flask_login import UserMixin, login_manager

class User(UserMixin):

	def __init__(self, _id):
	    self.id = _id
	    
	@staticmethod
	def validate_login(password_hash, password):
	    return check_password_hash(password_hash, password)


"""
@login_manager.user_loader
def user_loader(email):
	check = db.users.find_one({"email":email})

	if not check:
		return

	user = User(email)
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

	user = User(email)
	#user.id = email

	user.is_authenticated = User.validate_login(check['password'],request.form['password'])


	return user
"""