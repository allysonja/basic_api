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

if __name__ == '__main__':
    app.run(debug=True)