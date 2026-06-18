from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from app.models.product import Product, db
from app.models.order import Order
from app.utils.auth import require_admin
import os

admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route("/")
@require_admin
def admin_panel():

    search = request.args.get("search")

    if search:
        productos = Product.query.filter(Product.nombre.contains(search)).all()
    else:
        productos = Product.query.all()

    return render_template("admin.html", productos=productos, search=search)


@admin.route("/dashboard")
@require_admin
def dashboard():

    productos = Product.query.all()

    return render_template(
        "dashboard.html",
        total_productos=len(productos),
        stock_total=sum(p.stock for p in productos),
        valor_inventario=sum(p.precio * p.stock for p in productos)
    )


@admin.route("/create", methods=["POST"])
@require_admin
def create_product():

    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = float(request.form["precio"])
    stock = int(request.form.get("stock", 0))

    imagen_file = request.files["imagen"]
    filename = None

    if imagen_file and imagen_file.filename != "":
        filename = secure_filename(imagen_file.filename)
        ruta = os.path.join("app/static/images/products", filename)
        imagen_file.save(ruta)

    db.session.add(Product(
        nombre=nombre,
        descripcion=descripcion,
        precio=precio,
        stock=stock,
        imagen=filename
    ))
    db.session.commit()

    return redirect(url_for("admin.admin_panel"))


@admin.route("/edit/<int:id>", methods=["GET", "POST"])
@require_admin
def edit_product(id):

    producto = Product.query.get_or_404(id)

    if request.method == "POST":
        producto.nombre = request.form["nombre"]
        producto.descripcion = request.form["descripcion"]
        producto.precio = float(request.form["precio"])
        producto.stock = int(request.form["stock"])
        db.session.commit()
        return redirect(url_for("admin.admin_panel"))

    return render_template("edit.html", producto=producto)


@admin.route("/orders")
@require_admin
def orders():
    pedidos = Order.query.order_by(Order.created_at.desc()).all()
    return render_template("admin/orders.html", pedidos=pedidos)


@admin.route("/delete/<int:id>")
@require_admin
def delete_product(id):

    producto = Product.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()

    return redirect(url_for("admin.admin_panel"))
