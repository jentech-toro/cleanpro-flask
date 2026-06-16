from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Product(db.Model):

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(100), nullable=False)

    descripcion = db.Column(db.String(250))

    precio = db.Column(db.Float, nullable=False)

    imagen = db.Column(db.String(250))

    stock = db.Column(db.Integer, default=0)

    destacado = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Product {self.nombre}>"