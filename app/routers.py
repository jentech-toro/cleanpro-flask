from flask import Blueprint, render_template, request, redirect, url_for
from app.models.product import Product, db
import os
from werkzeug.utils import secure_filename
from flask import session


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

    if not session.get("admin"):
        return redirect(url_for("main.login"))

    search = request.args.get("search")

    if search:
        productos = Product.query.filter(
            Product.nombre.contains(search)
        ).all()
    else:
        productos = Product.query.all()

    return render_template(
        "admin.html",
        productos=productos,
        search=search
    )

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

    if not session.get("admin"):
        return redirect(url_for("main.login"))

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



@main.route("/add-to-cart/<int:id>")
def add_to_cart(id):

    producto = Product.query.get_or_404(id)

    cart = session.get("cart", {})

    cantidad = cart.get(str(id), 0)

    if cantidad < producto.stock:
        cart[str(id)] = cantidad + 1

    session["cart"] = cart

    return redirect(url_for("main.cart"))


@main.route("/cart")
def cart():

    cart = session.get("cart", {})

    if isinstance(cart, list):
        new_cart = {}
        for item in cart:
            new_cart[str(item)] = new_cart.get(str(item), 0) + 1
        cart = new_cart
        session["cart"] = cart

    ids = [int(i) for i in cart.keys()] if cart else []

    productos = Product.query.filter(Product.id.in_(ids)).all() if ids else []

    total = 0

    productos_con_cantidad = []

    for p in productos:
        cantidad = cart.get(str(p.id), 0)
        subtotal = p.precio * cantidad
        total += subtotal

        productos_con_cantidad.append({
            "producto": p,
            "cantidad": cantidad,
            "subtotal": subtotal
        })

    total = round(total, 2)

    mensaje = "Hola, quiero comprar:%0A"

    for item in productos_con_cantidad:
        p = item["producto"]
        mensaje += f"- {p.nombre} x{item['cantidad']} = ${item['subtotal']}%0A"

    mensaje += f"%0ATotal: ${total}"

    return render_template(
        "cart.html",
        items=productos_con_cantidad,
        total=total,
        mensaje=mensaje
    )

@main.route("/checkout", methods=["GET"])
def checkout():

    return render_template("checkout.html")


@main.route("/remove-from-cart/<int:id>")
def remove_from_cart(id):

    cart = session.get("cart", {})

    key = str(id)

    if key in cart:
        del cart[key]

    session["cart"] = cart

    return redirect(url_for("main.cart"))

@main.route("/decrease-cart/<int:id>")
def decrease_cart(id):

    cart = session.get("cart", {})

    key = str(id)

    if key in cart:

        cart[key] -= 1

        if cart[key] <= 0:
            del cart[key]

    session["cart"] = cart

    return redirect(url_for("main.cart"))

@main.route("/clear-cart")
def clear_cart():
    session.pop("cart", None)
    return redirect(url_for("main.cart"))

@main.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "123456":

            session["admin"] = True

            return redirect(url_for("main.dashboard"))

        return render_template(
            "login.html",
            error="Usuario o contraseña incorrectos"
        )

    return render_template("login.html")


@main.route("/logout")
def logout():

    session.pop("admin", None)

    return redirect(url_for("main.home"))

from flask import send_file
from app.utils.pdf_generator import generar_pedido_pdf

@main.route("/checkout", methods=["GET", "POST"])
def checkout():

    cart = session.get("cart", {})

    if not cart:
        return redirect(url_for("main.cart"))

    ids = [int(i) for i in cart.keys()]

    productos = Product.query.filter(Product.id.in_(ids)).all()

    items = []

    total = 0

    for p in productos:

        cantidad = cart.get(str(p.id), 0)

        subtotal = p.precio * cantidad

        total += subtotal

        items.append({
            "producto": p,
            "cantidad": cantidad,
            "subtotal": subtotal
        })

    if request.method == "POST":

        cliente = request.form["nombre"]

        archivo = "pedido.pdf"

        generar_pedido_pdf(
            archivo,
            cliente,
            items,
            total
        )

        session.pop("cart", None)

        return send_file(
            archivo,
            as_attachment=True
        )

    return render_template(
        "checkout.html",
        items=items,
        total=round(total, 2)
    )

