from app.models.product import db


class Customer(db.Model):

    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120))
    direccion = db.Column(db.String(250))

    orders = db.relationship("Order", backref="customer", lazy=True)
