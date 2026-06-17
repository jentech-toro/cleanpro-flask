from app import create_app
from app.models.product import Product, db

app = create_app()

with app.app_context():

    productos = Product.query.all()

    if len(productos) >= 3:
        productos[0].imagen = "cloro.jpg"
        productos[1].imagen = "desinfetante.jpg"
        productos[2].imagen = "escoba.jpg"
        productos[3].imagen = "guantes.jpg"

        db.session.commit()

        print("✅ Imágenes actualizadas correctamente")

    else:
        print("⚠️ No hay suficientes productos")