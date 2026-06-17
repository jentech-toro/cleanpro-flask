from flask import Blueprint, render_template, request, redirect, url_for
from app.models.product import Product, db
import os
from werkzeug.utils import secure_filename


main = Blueprint("main", __name__)


@main.route("/")
def home():

    servicios = [
        {
            "icono": "🏢",
            "titulo": "Limpieza de Oficinas",
            "descripcion": "Espacios corporativos impecables."
        },
        {
            "icono": "🏠",
            "titulo": "Limpieza del Hogar",
            "descripcion": "Ambientes limpios y saludables."
        },
        {
            "icono": "🧹",
            "titulo": "Limpieza Profunda",
            "descripcion": "Resultados profesionales garantizados."
        }
    ]

    productos = Product.query.all()

    return render_template(
        "index.html",
        servicios=servicios,
        productos=productos
    )


@main.route("/admin")
def admin():

    search = request.args.get("search")

    if search:
        productos = Product.query.filter(
            Product.nombre.contains(search)
        ).all()
    else:
        productos = Product.query.all()

    return render_template("admin.html", productos=productos, search=search)

@main.route("/admin/create", methods=["POST"])
def create_product():

    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    stock = request.form["stock"]

    imagen_file = request.files["imagen"]

    filename = None

    if imagen_file and imagen_file.filename != "":
        filename = secure_filename(imagen_file.filename)
        ruta = os.path.join("app/static/images/products", filename)
        imagen_file.save(ruta)

    nuevo = Product(
        nombre=nombre,
        descripcion=descripcion,
        precio=float(precio),
        stock=int(stock) if stock else 0,
        imagen=filename
    )

    from app.models.product import db
    db.session.add(nuevo)
    db.session.commit()

    return redirect(url_for("main.admin"))

@main.route("/admin/delete/<int:id>")
def delete_product(id):

    producto = Product.query.get_or_404(id)

    from app import db
    db.session.delete(producto)
    db.session.commit()

    return redirect(url_for("main.admin"))

@main.route("/admin/edit/<int:id>", methods=["GET", "POST"])
def edit_product(id):

    producto = Product.query.get_or_404(id)

    if request.method == "POST":

        producto.nombre = request.form["nombre"]
        producto.descripcion = request.form["descripcion"]
        producto.precio = float(request.form["precio"])
        producto.stock = int(request.form["stock"])

        from app.models.product import db
        db.session.commit()

        return redirect(url_for("main.admin"))

    return render_template("edit.html", producto=producto)

@main.route("/dashboard")
def dashboard():

    productos = Product.query.all()

    total_productos = len(productos)

    stock_total = sum(p.stock for p in productos)

    valor_inventario = sum(p.precio * p.stock for p in productos)

    return render_template(
    "dashboard.html",
    total_productos=total_productos,
    stock_total=stock_total,
    valor_inventario=valor_inventario
)

from flask import session

@main.route("/add-to-cart/<int:id>")
def add_to_cart(id):

    cart = session.get("cart", [])

    cart.append(id)

    session["cart"] = cart

    return redirect(url_for("main.home"))

@main.route("/cart")
def cart():

    cart_ids = session.get("cart", [])

    productos = Product.query.filter(Product.id.in_(cart_ids)).all()

    return render_template("cart.html", productos=productos)