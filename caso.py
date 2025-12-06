from flask import request, jsonify
import pandas as pd

# Lista donde se guardan los casos ingresados
casos = []


# --------------------- CREAR CASO ---------------------
def crear_caso():
    data = request.get_json()

    caso = {
        "edad_victima": data.get("edad_victima"),
        "sexo_victima": data.get("sexo_victima"),
        "relacion_agresor": data.get("relacion_agresor"),
        "sexo_agresor": data.get("sexo_agresor"),
        "convivencia": data.get("convivencia")
    }

    casos.append(caso)
    return jsonify({"mensaje": "Caso registrado"}), 201



# --------------------- ESTADÍSTICA: SEXO VÍCTIMA ---------------------
def stats_sexo_victima():
    if not casos:
        return jsonify({})

    df = pd.DataFrame(casos)
    conteo = df["sexo_victima"].value_counts().to_dict()

    return jsonify(conteo)



# --------------------- ESTADÍSTICA: RELACIÓN CON EL AGRESOR ---------------------
def stats_relacion():
    if not casos:
        return jsonify({})

    df = pd.DataFrame(casos)
    conteo = df["relacion_agresor"].value_counts().to_dict()

    return jsonify(conteo)


def stats_edad():
    if not casos:
        return jsonify([])

    df = pd.DataFrame(casos)
    edades = df["edad_victima"].astype(int).tolist()

    return jsonify(edades)
