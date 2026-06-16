from app import create_app
from app.models.product import db, Product

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    p1 = Product(
        nombre="Cloro Industrial",
        descripcion="Desinfectante fuerte para superficies",
        precio=9.99,
        stock=50
    )

    p2 = Product(
        nombre="Escoba Pro",
        descripcion="Uso industrial resistente",
        precio=14.99,
        stock=30
    )

    db.session.add_all([p1, p2])
    db.session.commit()

    print("✔ Productos creados correctamente")