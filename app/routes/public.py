from flask import Blueprint, render_template, request, redirect, url_for, session, send_file
from app.models.product import Product, db
from app.models.customer import Customer
from app.models.order import Order, OrderItem
from app.utils.pdf_generator import generate_order_pdf
import os

public = Blueprint("public", __name__)

SERVICIOS = [
    {"icono": "🏢", "titulo": "Limpieza de Oficinas", "descripcion": "Espacios corporativos impecables."},
    {"icono": "🏠", "titulo": "Limpieza del Hogar", "descripcion": "Ambientes limpios y saludables."},
    {"icono": "🧹", "titulo": "Limpieza Profunda", "descripcion": "Resultados profesionales garantizados."},
]


@public.route("/")
def home():
    return render_template("index.html", servicios=SERVICIOS, productos=Product.query.all())


def _build_cart_items(cart):
    ids = [int(i) for i in cart.keys()] if cart else []
    productos = Product.query.filter(Product.id.in_(ids)).all() if ids else []

    items = []
    total = 0

    for p in productos:
        cantidad = cart.get(str(p.id), 0)
        subtotal = round(p.precio * cantidad, 2)
        total += subtotal
        items.append({"producto": p, "cantidad": cantidad, "subtotal": subtotal})

    return items, round(total, 2)


@public.route("/cart")
def cart():

    raw = session.get("cart", {})

    if isinstance(raw, list):
        fixed = {}
        for item in raw:
            fixed[str(item)] = fixed.get(str(item), 0) + 1
        raw = fixed
        session["cart"] = raw

    items, total = _build_cart_items(raw)

    mensaje = "Hola, quiero comprar:%0A"
    for item in items:
        p = item["producto"]
        mensaje += f"- {p.nombre} x{item['cantidad']} = ${item['subtotal']}%0A"
    mensaje += f"%0ATotal: ${total}"

    return render_template("cart.html", items=items, total=total, mensaje=mensaje)


@public.route("/add-to-cart/<int:id>")
def add_to_cart(id):

    producto = Product.query.get_or_404(id)
    cart = session.get("cart", {})
    cantidad = cart.get(str(id), 0)

    if cantidad < producto.stock:
        cart[str(id)] = cantidad + 1

    session["cart"] = cart
    return redirect(url_for("public.cart"))


@public.route("/remove-from-cart/<int:id>")
def remove_from_cart(id):

    cart = session.get("cart", {})
    cart.pop(str(id), None)
    session["cart"] = cart
    return redirect(url_for("public.cart"))


@public.route("/decrease-cart/<int:id>")
def decrease_cart(id):

    cart = session.get("cart", {})
    key = str(id)

    if key in cart:
        cart[key] -= 1
        if cart[key] <= 0:
            del cart[key]

    session["cart"] = cart
    return redirect(url_for("public.cart"))


@public.route("/clear-cart")
def clear_cart():
    session.pop("cart", None)
    return redirect(url_for("public.cart"))


@public.route("/checkout", methods=["GET", "POST"])
def checkout():

    cart = session.get("cart", {})

    if not cart:
        return redirect(url_for("public.cart"))

    items, total = _build_cart_items(cart)

    if request.method == "POST":
        nombre = request.form["nombre"]
        telefono = request.form.get("telefono", "")
        email = request.form.get("email", "")

        customer = Customer(nombre=nombre, telefono=telefono, email=email)
        db.session.add(customer)
        db.session.flush()

        order = Order(total=total, customer_id=customer.id)
        db.session.add(order)
        db.session.flush()

        for item in items:
            db.session.add(OrderItem(
                order_id=order.id,
                product_id=item["producto"].id,
                cantidad=item["cantidad"],
                precio_unitario=item["producto"].precio,
                subtotal=item["subtotal"]
            ))

        db.session.commit()

        archivo = os.path.join(os.getcwd(), "pedido.pdf")
        generate_order_pdf(archivo, nombre, items, total)
        session.pop("cart", None)
        return send_file(archivo, as_attachment=True)

    return render_template("checkout.html", items=items, total=total)
