from flask import Blueprint, render_template

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

    return render_template(
        "index.html",
        servicios=servicios
    )