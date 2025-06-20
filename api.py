from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, marshal_with, fields, abort


app = Flask(__name__)  # Initialize Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # Database URI (SQLite in this case) 
db = SQLAlchemy(app) # Initialize SQLAlchemy
api = Api(app) # Initialize Flask-RESTful API


class UserModal(db.Model): # Define User model 
    id = db.Column(db.Integer, primary_key=True) # Primary key
    name = db.Column(db.String(80), unique=True, nullable=False) # Name field
    email = db.Column(db.String(120), unique=True, nullable=False) # Email field
    age = db.Column(db.Integer, nullable=False) # Age field

    def __repr__(self): # String representation
        return f"User (name = {self.name}, email = {self.email}, age = {self.age})" # Define how the User model is represented

user_args = reqparse.RequestParser() # Initialize request parser for user input

user_args.add_argument('name', type=str, help='Name cannot be blank', required=True) # Add name argument to parser

user_args.add_argument('email', type=str, help='Email cannot be blank', required=True) # Add email argument to parser

user_args.add_argument('age', type=int, help='Age cannot be blank', required=True) # Add age argument to parser

userFields = {
    'id': fields.Integer, # Define fields for marshalling
    'name': fields.String,
    'email': fields.String,
    'age': fields.Integer,
}

class Users(Resource): # Define Users resource for API
    @marshal_with(userFields) # Use marshalling to format output
    def get(self):
        users = UserModal.query.all()
        return users
    
    @marshal_with(userFields) # Use marshalling to format output
    def post(self):
        args = user_args.parse_args()
        user = UserModal(name=args['name'], email=args['email'], age=args['age'])
        db.session.add(user)
        db.session.commit()
        users = UserModal.query.all()
        return users, 201
    
class User(Resource): # Define User resource for API
    @marshal_with(userFields) # Use marshalling to format output
    def get(self, id):
        user = UserModal.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User not found")
        return user
    @marshal_with(userFields)
    def patch(self, id):
        args = user_args.parse_args() # Parse user input
        user = UserModal.query.filter_by(id=id).first() # Get user
        if not user:
            abort(404, message="User not found") # User not found
        user.name = args['name'] # Update name and email and age
        user.email = args['email']
        user.age = args['age']
        db.session.commit()
        return user
    @marshal_with(userFields)
    def delete(self, id):
        user = UserModal.query.filter_by(id=id).first() # Get user
        if not user:
            abort(404, message="User not found") # User not found
        db.session.delete(user)
        db.session.commit()
        users = UserModal.query.all()
        return users
    
api.add_resource(Users, '/api/users/') # Add Users resource to API with endpoint '/api/users/'
api.add_resource(User, '/api/users/<int:id>') # Add User resource to API with endpoint '/api/users/<id>'

@app.route('/') # Define home route for API endpoint

def home(): # Home route function
    return '<h1>Welcome to the Demo Project 2 API!</h1>'    # Return welcome message 

if __name__ == '__main__':  # Check if the script is run directly
     app.run(debug=True) # Run the Flask app in debug mode