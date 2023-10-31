"""Models for Cupcake app."""
# Imports
from flask_sqlalchemy import SQLAlchemy

# SetUp
db = SQLAlchemy()

# Models
class Cupcake(db.Model):
    """Cupcake Model"""
    __tablename__ = 'cupcakes'

    def __repr__(self):
        """Defines the way in which an instance represents itself"""
        cupcake = self
        return f"<Cupcake id={cupcake.id} flavor={cupcake.flavor} size={cupcake.size} rating={cupcake.rating}>"
    # Columns
    id = db.Column(db.Integer, 
                   primary_key = True, 
                   autoincrement = True)
    flavor = db.Column(db.Text,
                       nullable = False) 
    size = db.Column(db.Text,
                     nullable = False)
    rating = db.Column(db.Float,
                       nullable = False)
    image = db.Column(db.Text,
                      nullable = False,
                      default = 'https://tinyurl.com/demo-cupcake')
    #Methods
    def serialize(self):
        """Serialize a cupcake SQLAlchemy object to a dictionary"""
        return {
            "id" : self.id,
            "flavor" : self.flavor,
            "size" : self.size,
            "rating" : self.rating,
            "image" : self.image
        }
    

def connect_db(app):
    """Connect Application to Database"""
    db.app = app
    db.init_app(app)