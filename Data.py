
import pandas as pd


COLUMNAS = {
    "fecha_denuncia": "Fecha_Denuncia",
    "edad": "Edad_Victima",
    "unidad_edad": "Unidad_Edad",
    "edadA":"Edad_Victima_Anos",
    "sexo_victima": "Sexo_Victima",
    "estrato": "Estrato",
    "barrio": "Barrio_Victima",
    "area":"Area_Residencia",
    "seguridad":"Seguridad_Social",
    "orientacion":"Orientacion_Sexual",
    "consumoSPA":"Consumo_SPA",
    "alcohol":"Alcohol_SPA",
    "mecanismo": "Mecanismo_Agresion",
    "escenario": "ESCENARIO",
    "fecha_hecho": "Fecha_Hecho",
    "sexo_agresor": "Sexo_Agresor",
    "relacion": "Relacion_Victima",
    "convive": "Convive_Agresor",
    "antecedentes":"Antecedentes_Violencia",
}

# -------- DataFrame principal --------
def cargar_dataframe():
    df = pd.read_excel("ProyectoB_Limpio.xlsx")
    return df, COLUMNAS


# -------- Tablas adicionales de acoso --------
def cargar_tablas_acoso():
    tablas = []

    for i in range(1, 6):
        try:
            df = pd.read_excel(f"tabla_acoso_{i}.xlsx")

            df = df.rename(columns={
                "none": "valor_p",
                "none.1": "v_cramer",
                "none.2": "porcentaje"
            })

            tablas.append({
                "nombre": f"Tabla {i}",
                "columnas": df.columns.tolist(),
                "datos": df.to_dict(orient="records")
            })

        except Exception as e:
            print(f"Error cargando tabla {i}: {e}")

    return tablas
