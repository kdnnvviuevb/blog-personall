import os
from flask import Flask, render_template, request, redirect, url_for
import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def crear_app():
    app = Flask(__name__)

    cliente = MongoClient(os.getenv("MONGODB_URI"))
    app.db = cliente.blog

    @app.route("/", methods=["GET", "POST", "HEAD"])
    def home():
        if request.method == "POST":
            titulo = request.form.get("tit")
            entry = request.form.get("content")
            fecha_formato = datetime.datetime.today().strftime("%d-%m-%Y")

            parametros = {
                "titulo": titulo,
                "contenido": entry,
                "fecha": fecha_formato
            }

            app.db.contenido.insert_one集合(parametros)
            return redirect(url_for("home"))

        # GET y HEAD: solo mostrar la página
        entradas = list(app.db.contenido.find({}).sort("fecha", -1))
        return render_template("index.html", entradas=entradas)

    return app

if __name__ == "__main__":
    app = crear_app()
    app.run()
