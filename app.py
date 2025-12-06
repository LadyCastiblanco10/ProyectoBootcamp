from flask import Flask, render_template
from Hipotesis import via_publica, tiempo_denuncia, estrato, relacion_agresor, consumo_sustancias
from caso import crear_caso, stats_sexo_victima, stats_relacion, stats_edad

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/casos")
def casos_html():
    return render_template("casos.html")


# ------------------ ENDPOINTS CASOS ------------------
app.add_url_rule("/crearCaso", view_func=crear_caso, methods=["POST"])
app.add_url_rule("/estadisticas/sexoVictima", view_func=stats_sexo_victima)
app.add_url_rule("/estadisticas/relacionAgresor", view_func=stats_relacion)
app.add_url_rule("/estadisticas/edadVictima", view_func=stats_edad)



# ------------------ ENDPOINTS HIPÓTESIS ------------------
app.add_url_rule("/via-publica", view_func=via_publica)
app.add_url_rule("/tiempo-denuncia", view_func=tiempo_denuncia)
app.add_url_rule("/estrato", view_func=estrato)
app.add_url_rule("/relacion-agresor", view_func=relacion_agresor)
app.add_url_rule("/consumo", view_func=consumo_sustancias)


if __name__ == "__main__":
    app.run(debug=True)
