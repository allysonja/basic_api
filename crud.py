from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin
from sqlalchemy import text
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	email = db.Column(db.String(120), unique=True)

	def __init__(self, username, email):
		self.username = username
		self.email = email

class UserSchema(ma.Schema):
	class Meta:
		# Fields to expose
		fields = ("username", "email")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# endpoint to show all users
@app.route("/user", methods=["GET"])
def get_user():
	all_users = User.query.all()
	result = users_schema.dump(all_users)
	return jsonify(result.data)

# endpoint to create new user
@app.route("/user", methods=["POST"])
def add_user():
	username = request.json['username']
	email = request.json['email']

	username = username.lower()
	email = email.lower()

	new_user = User(username, email)
	result = user_schema.dump(new_user)

	db.session.add(new_user)
	db.session.commit()

	return jsonify(result)

# endpoint to get user details by id
@app.route("/user/<id>", methods=["GET"])
def user_detail(id):
	user = User.query.get(id)
	return user_schema.jsonify(user)

# endpoint to update user
@app.route("/user/<id>", methods=["PUT"])
def user_update(id):
	user = User.query.get(id)
	username = request.json['username']
	email = request.json['email']

	user.username = username
	user.email = email

	result = user_schema.dump(user)

	db.session
	db.session.commit()

	return user_schema.jsonify(user)

# endpoint to delete user
@app.route("/user/<id>", methods=["DELETE"])
def user_delete(id):
	user = User.query.get(id)
	db.session.delete(user)
	db.session.commit()

	return user_schema.jsonify(user)

# endpoint to get list of usernames in database
@app.route("/userlist", methods=["GET"])
def user_list():
	sqlquery = "SELECT username FROM user"
	all_usernames = db.engine.execute(sqlquery)
	result = []
	for row in all_usernames:
		result.append(row[0])
	return jsonify(result)

# endpoint to get list of emails in database
@app.route("/emaillist", methods=["GET"])
def email_list():
	sqlquery = "SELECT email FROM user"
	all_emails = db.engine.execute(sqlquery)
	result = []
	for row in all_emails:
		result.append(row[0])
	return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)