from flask import Blueprint, render_template
from app.models.product import Product
from flask import request, redirect, url_for


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

    productos = Product.query.all()

    return render_template("admin.html", productos=productos)

@main.route("/admin/create", methods=["POST"])
def create_product():

    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    stock = request.form["stock"]

    nuevo = Product(
        nombre=nombre,
        descripcion=descripcion,
        precio=float(precio),
        stock=int(stock) if stock else 0
    )



    from app import db
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

        from app import db
        db.session.commit()

        return redirect(url_for("main.admin"))

    return render_template("edit.html", producto=producto)