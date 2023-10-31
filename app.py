"""Flask app for Cupcakes"""
# Imports / Configurations

from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.debug = True

app.config['SECRET_KEY'] = 'T00$3cr3t4M3'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cupcakes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.app_context().push()

connect_db(app)

# Routes
    
# Home Page
@app.route('/')
def show_homepage():
    """Render homepage"""
    
    return render_template('index.html')

# API Routes
@app.route('/api/cupcakes')
def get_cupcakes():
    """Get data about all cupcakes.
    
    Respond with JSON: {cupcakes: [{id, flavor, size, rating, image}, ...]}"""

    cupcakes = Cupcake.query.all()
    serialized = [cupcake.serialize() for cupcake in cupcakes]
    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create dessert from data and return it."""

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]
    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    return (jsonify(cupcake=new_cupcake.serialize()), 201)

@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """Get data about a single cupcake.
    
    Respond with JSON: {cupcake: {id, flavor, size, rating, image}}"""

    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake = cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    """Update a cupcake with the id passed in the URL and flavor, size, rating and image data from the body of the request. 
    This should raise a 404 if the cupcake cannot be found.
    
    Respond with JSON of the newly-updated cupcake, like this: {cupcake: {id, flavor, size, rating,image}}"""

    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.commit()
    return jsonify(cupcake = cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
    """This should raise a 404 if the cupcake cannot be found. Delete cupcake with the id passed in the URL
    
    Respond with JSON like {message: "Deleted"}"""

    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted.")
