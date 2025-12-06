
from flask import render_template
import pandas as pd
import matplotlib.pyplot as plt
import os
from Data import cargar_dataframe, cargar_tablas_acoso

import matplotlib
matplotlib.use("Agg")


# =====================================================
# 🔹 HIPÓTESIS — VÍA PÚBLICA
# =====================================================
def via_publica():

    tablas_extra = cargar_tablas_acoso()
    tablas_extra = [tablas_extra[i] for i in [0, 3, 4] if i < len(tablas_extra)]

    df, col = cargar_dataframe()

    # Normalizar ESCENARIO
    df[col["escenario"]] = (
        df[col["escenario"]]
        .astype(str)
        .str.normalize("NFKD")
        .str.encode("ascii", "ignore")
        .str.decode("ascii")
        .str.upper()
    )

    palabras_via = ["VIA", "PUBLICA", "CALLE", "PARQUE", "TRANSITO", "TRANSPORTE"]

    df_via = df[df[col["escenario"]].apply(
        lambda x: any(p in x for p in palabras_via)
    )]

    if df_via.empty:
        return "No se encontraron registros de vía pública."

    columnas_mostrar = [
        col["edad"],
        col["unidad_edad"],
        col["sexo_victima"],
        col["sexo_agresor"],
        col["relacion"],
        col["mecanismo"]
    ]

    df_via = df_via[columnas_mostrar]

    tabla_json = df_via.to_dict(orient="records")
    columnas_tabla = columnas_mostrar

    os.makedirs("static/graficas", exist_ok=True)

    # G1 - Víctimas por sexo
    plt.figure(figsize=(12, 7))
    df_via[col["sexo_victima"]].value_counts().plot(kind="bar")
    plt.title("Víctimas por sexo en vía pública")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/graficas/via_genero.png")
    plt.close()

    # G2 - Distribución de edades
    plt.figure(figsize=(12, 7))
    df_via[col["edad"]].plot(kind="hist", bins=20)
    plt.title("Distribución de edades de víctimas")
    plt.tight_layout()
    plt.savefig("static/graficas/via_edad.png")
    plt.close()

    # G3 - Mecanismos de agresión
    plt.figure(figsize=(12, 7))
    df_via[col["mecanismo"]].value_counts().head(10).plot(kind="bar")
    plt.title("Métodos de agresión más frecuentes")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/graficas/via_mecanismo.png")
    plt.close()

    # G4 - Cruce agresor/víctima
    plt.figure(figsize=(12, 7))
    pd.crosstab(df_via[col["sexo_agresor"]], df_via[col["sexo_victima"]]).plot(kind="bar")
    plt.title("Cruce: Sexo agresor / Sexo víctima")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/graficas/via_agresor_vs_victima.png")
    plt.close()

    return render_template(
        "HI-ViaPublica.html",
        g1="graficas/via_genero.png",
        g2="graficas/via_edad.png",
        g3="graficas/via_mecanismo.png",
        g4="graficas/via_agresor_vs_victima.png",
        tabla=tabla_json,
        columnas=columnas_tabla,
        tablas_extra=tablas_extra
    )


# =====================================================
# 🔹 HIPÓTESIS — TIEMPO ENTRE HECHO Y DENUNCIA
# =====================================================
def tiempo_denuncia():
    
    df, col = cargar_dataframe()

    # Normalizar RELACIÓN
    df[col["relacion"]] = (
    df[col["relacion"]]
    .astype(str)
    .str.strip()
    .str.normalize("NFKD")
    .str.encode("ascii", "ignore")
    .str.decode("ascii")
    .str.upper()
)

# Unificar variantes
    df[col["relacion"]] = df[col["relacion"]].replace({
    "EX PAREJA": "EXPAREJA",
    "EX-PAREJA": "EXPAREJA"
})


    
    os.makedirs("static/graficas_tiempo", exist_ok=True)
    

    


    # CALCULAR DÍAS ENTRE HECHO Y DENUNCIA
   
    df["fecha_d"] = pd.to_datetime(df[col["fecha_denuncia"]], errors="coerce")
    df["fecha_h"] = pd.to_datetime(df[col["fecha_hecho"]], errors="coerce")
    df["dias_espera"] = (df["fecha_d"] - df["fecha_h"]).dt.days

    # Eliminar valores absurdos
    df = df[df["dias_espera"].between(0, 365)]   # Hasta 1 año
    df = df.dropna(subset=["dias_espera"])

  
    # TABLA 
    columnas_mostrar = [
        col["edad"],
        col["unidad_edad"],
        col["sexo_victima"],
        col["sexo_agresor"],
        col["relacion"],
        col["antecedentes"],
        "dias_espera"
    ]

    df_tabla = df[columnas_mostrar]
    tabla_json = df_tabla.to_dict(orient="records")
    columnas_tabla = columnas_mostrar

    # ================================
    # GRÁFICAS
    # ================================

    # G1 - Histograma
    plt.figure(figsize=(11, 5))
    plt.hist(df["dias_espera"], bins=40)
    plt.title("Distribución del tiempo entre el hecho y la denuncia")
    plt.xlabel("Días de espera")
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    plt.savefig("static/graficas_tiempo/tiempo_hist.png")
    plt.close()

    # G2 - Promedio por sexo de víctima
    plt.figure(figsize=(8, 5))
    df.groupby(col["sexo_victima"])["dias_espera"].mean().plot(kind="bar")
    plt.title("Promedio de días según sexo de la víctima")
    plt.ylabel("Promedio (días)")
    plt.tight_layout()
    plt.savefig("static/graficas_tiempo/tiempo_sexo.png")
    plt.close()

    # G3 - Relación víctima–agresor
    plt.figure(figsize=(12, 6))
    df.groupby(col["relacion"])["dias_espera"].mean().sort_values().plot(kind="bar")
    plt.title("Tiempo promedio según relación víctima–agresor")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/graficas_tiempo/tiempo_relacion.png")
    plt.close()

    # G4 - Antecedentes y tiempo de denuncia
    plt.figure(figsize=(10, 5))
    df.groupby(col["antecedentes"])["dias_espera"].mean().sort_values().plot(kind="bar")
    plt.title("Tiempo promedio según antecedentes")
    plt.ylabel("Promedio (días)")
    plt.tight_layout()
    plt.savefig("static/graficas_tiempo/tiempo_antecedentes.png")
    plt.close()

    return render_template(
        "HI-TiempoDenuncia.html",
        g1="graficas_tiempo/tiempo_hist.png",
        g2="graficas_tiempo/tiempo_sexo.png",
        g3="graficas_tiempo/tiempo_relacion.png",
        g4="graficas_tiempo/tiempo_antecedentes.png",
        tabla=tabla_json,
        columnas=columnas_tabla
    )



# =====================================================
# 🔹 HIPÓTESIS — ESTRATO Y ENTORNO SOCIAL
# =====================================================
def estrato():

    df, col = cargar_dataframe()

    os.makedirs("static/graficas_estrato", exist_ok=True)

    # ================================
    # LIMPIEZA BÁSICA
    # ================================
    df[col["estrato"]] = (
    pd.to_numeric(df[col["estrato"]], errors="coerce")
    .astype("Int64")
)

    df = df.dropna(subset=[col["estrato"]])

    # ================================
    # TABLA QUE SE MOSTRARÁ
    # ================================
    columnas_mostrar = [
        col["estrato"],
        col["barrio"],               
        col["area"],
        col["sexo_victima"],
        col["edad"],
        col["sexo_agresor"],
        col["relacion"]
    ]

    # Filtrar solo columnas existentes
    columnas_mostrar = [c for c in columnas_mostrar if c in df.columns]

    df_tabla = df[columnas_mostrar]
    tabla_json = df_tabla.to_dict(orient="records")
    columnas_tabla = columnas_mostrar

    # ================================
    # GRÁFICAS
    # ================================

    # G1 - Distribución del estrato
    plt.figure(figsize=(10,5))
    df[col["estrato"]].value_counts().sort_index().plot(kind="bar")
    plt.title("Distribución de estratos socioeconómicos")
    plt.xlabel("Estrato")
    plt.ylabel("Cantidad de casos")
    plt.tight_layout()
    plt.savefig("static/graficas_estrato/estrato_distrib.png")
    plt.close()

    # G2 - Estrato por edad de víctima
    df[col["edad"]] = pd.to_numeric(df[col["edad"]], errors="coerce")

# Quitar edades inválidas (0 o negativas)
    df = df[df[col["edad"]] >= 1]

# Crear rangos de edad
    bins = [1, 10, 20, 30, 40, 50, 60, 120]
    labels = [
    "1-10", "11-20", "21-30", "31-40",
    "41-50", "51-60", "61+"
]

    df["edad_rango"] = pd.cut(df[col["edad"]], bins=bins, labels=labels, right=True)

    plt.figure(figsize=(10,6))
    df.groupby("edad_rango")[col["estrato"]].mean().plot(kind="bar")

    plt.title("Estrato promedio según rango de edad de la víctima")
    plt.ylabel("Estrato promedio")
    plt.xlabel("Rango de edad")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig("static/graficas_estrato/estrato_edad.png")
    plt.close()

    # G3 - Estrato por área residencial
    plt.figure(figsize=(12,6))
    df.groupby(col["area"])[col["estrato"]].mean().sort_values().plot(kind="bar")
    plt.title("Estrato promedio por área residencial")
    plt.ylabel("Estrato promedio")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/graficas_estrato/estrato_area.png")
    plt.close()

  # G4 - Estrato promedio por barrio (Gráfico de burbujas)
    grupo = (
    df.groupby(col["barrio"])[col["estrato"]]
    .mean()
    .round(2)
    .to_frame("estrato_promedio")
)

# Agregar frecuencia para filtrar barrios relevantes
    grupo["cantidad"] = df.groupby(col["barrio"]).size()

# Quedarse con los 20 barrios con más casos
    grupo = grupo.sort_values("cantidad", ascending=False).head(20) 

    plt.figure(figsize=(12,6))
    grupo["estrato_promedio"].sort_values().plot(kind="bar")

    plt.title("Estrato promedio por 20 barrios con más casos")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/graficas_estrato/estrato_barrio.png")
    plt.close()





    return render_template(
        "HI-Estrato.html",
        g1="graficas_estrato/estrato_distrib.png",
        g2="graficas_estrato/estrato_edad.png",
        g3="graficas_estrato/estrato_area.png",
        g4="graficas_estrato/estrato_barrio.png",
        tabla=tabla_json,
        columnas=columnas_tabla
    )

# =====================================================
# 🔹 RelacionAgresor
# =====================================================
def relacion_agresor():
    
    df, col = cargar_dataframe()

    os.makedirs("static/graficas_relacion_agresor", exist_ok=True)

    # ================================
    # LIMPIEZA BÁSICA
    # ================================
    df[col["edad"]] = pd.to_numeric(df[col["edad"]], errors="coerce")
    df = df[df[col["edad"]] >= 1]  # quitar edades inválidas

    # Crear rangos de edad
    bins = [1, 10, 20, 30, 40, 50, 60, 120]
    labels = ["1-10", "11-20", "21-30", "31-40", "41-50", "51-60", "61+"]
    df["edad_rango"] = pd.cut(df[col["edad"]], bins=bins, labels=labels, right=True)

    # ================================
    # TABLA QUE SE MOSTRARÁ
    # ================================
    columnas_mostrar = [
        col["relacion"],
        col["edad"],
        col["convive"],
        col["antecedentes"],
        col["sexo_victima"],
        col["sexo_agresor"]
    ]

    columnas_mostrar = [c for c in columnas_mostrar if c in df.columns]

    df_tabla = df[columnas_mostrar]
    tabla_json = df_tabla.to_dict(orient="records")

    # ================================
    # G1 — Distribución de tipo de relación
    # ================================
    plt.figure(figsize=(12, 6))
    df[col["relacion"]].value_counts().plot(kind="bar")
    plt.title("Distribución de relaciones entre víctima y agresor")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/graficas_relacion_agresor/relacion_distrib.png")
    plt.close()

    # ================================
    # G2 — Relación × Rango de edad
    # ================================
    plt.figure(figsize=(12,6))
    df.groupby([col["relacion"], "edad_rango"]).size().unstack().plot(kind="bar", stacked=True, figsize=(12,6))
    plt.title("Relación víctima–agresor según rango de edad")
    plt.ylabel("Cantidad")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/graficas_relacion_agresor/relacion_edad_rangos.png")
    plt.close()

    # ================================
    # G3 — Relación × Convive (Sí / No)
    # ================================
    plt.figure(figsize=(12,6))
    df.groupby([col["relacion"], col["convive"]]).size().unstack().plot(kind="bar", figsize=(12,6))
    plt.title("Relación víctima–agresor según convivencia")
    plt.ylabel("Cantidad")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/graficas_relacion_agresor/relacion_convive.png")
    plt.close()

    # ================================
    # G4 — Relación × Antecedentes de violencia
    # ================================
    plt.figure(figsize=(12,6))
    df.groupby([col["relacion"], col["antecedentes"]]).size().unstack().plot(kind="bar", stacked=True, figsize=(12,6))
    plt.title("Relación víctima–agresor según antecedentes de violencia")
    plt.ylabel("Cantidad")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/graficas_relacion_agresor/relacion_antecedentes.png")
    plt.close()

    # ================================
    # G5 — Heatmap Sexo víctima × sexo agresor
    # ================================
    tabla_heatmap = df.pivot_table(
        index=col["sexo_victima"],
        columns=col["sexo_agresor"],
        values=col["relacion"],
        aggfunc='count',
        fill_value=0
    )

    plt.figure(figsize=(8,6))
    plt.imshow(tabla_heatmap, cmap="Blues")
    plt.colorbar(label="Cantidad de casos")
    plt.xticks(range(len(tabla_heatmap.columns)), tabla_heatmap.columns, rotation=45)
    plt.yticks(range(len(tabla_heatmap.index)), tabla_heatmap.index)
    plt.title("Heatmap sexo víctima vs sexo agresor")
    plt.tight_layout()
    plt.savefig("static/graficas_relacion_agresor/relacion_sexos_heatmap.png")
    plt.close()

    # ================================
    # RETORNAR TEMPLATE
    # ================================
    return render_template(
        "HI-RelacionAgresor.html",
        g1="graficas_relacion_agresor/relacion_distrib.png",
        g2="graficas_relacion_agresor/relacion_edad_rangos.png",
        g3="graficas_relacion_agresor/relacion_convive.png",
        g4="graficas_relacion_agresor/relacion_antecedentes.png",
        g5="graficas_relacion_agresor/relacion_sexos_heatmap.png",
        tabla=tabla_json,
        columnas=columnas_mostrar
    )


# =====================================================
# 🔹 Consumo de Sustancias Psicoactivas (SPA y Alcohol)
# =====================================================
def consumo_sustancias():

    df, col = cargar_dataframe()

    os.makedirs("static/graficas_spa", exist_ok=True)

    # ================================
    # LIMPIEZA BÁSICA
    # ================================
    df[col["edad"]] = pd.to_numeric(df[col["edad"]], errors="coerce")
    df = df[df[col["edad"]] >= 1]  # quitar edades inválidas

    # Rangos de edad
    bins = [1, 10, 20, 30, 40, 50, 60, 120]
    labels = ["1–10", "11–20", "21–30", "31–40", "41–50", "51–60", "61+"]
    df["edad_rango"] = pd.cut(df[col["edad"]], bins=bins, labels=labels, right=True)

    # ================================
    # TABLA MOSTRADA EN HTML
    # ================================
    columnas_mostrar = [
        col["consumoSPA"],
        col["alcohol"],
        col["mecanismo"],
        col["sexo_victima"],
        col["edad"],
        "edad_rango",
        col["relacion"]
    ]

    df_tabla = df[columnas_mostrar]
    tabla_json = df_tabla.to_dict(orient="records")

    # =====================================================
    # G1 — Distribución del consumo de SPA
    # =====================================================
    plt.figure(figsize=(12, 6))
    df[col["consumoSPA"]].value_counts().plot(kind="bar")
    plt.title("Consumo de Sustancias Psicoactivas (SPA)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/graficas_spa/spa_distrib.png")
    plt.close()

    # =====================================================
    # G2 — Consumo de alcohol (Sí/No)
    # =====================================================
    plt.figure(figsize=(12, 6))
    df[col["alcohol"]].value_counts().plot(kind="bar", color="orange")
    plt.title("Consumo de alcohol por parte del agresor")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/graficas_spa/alcohol_distrib.png")
    plt.close()

    # =====================================================
    # G3 — Consumo de SPA según sexo de la víctima
    # =====================================================
    plt.figure(figsize=(12, 6))
    df.groupby([col["sexo_victima"], col["consumoSPA"]]).size().unstack().plot(
        kind="bar", figsize=(12, 6)
    )
    plt.title("Consumo de SPA según el sexo de la víctima")
    plt.ylabel("Cantidad")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/graficas_spa/spa_sexo_victima.png")
    plt.close()

    # =====================================================
    # G4 — Relación víctima–agresor × Consumo de SPA
    # =====================================================
    plt.figure(figsize=(12, 6))
    df.groupby([col["relacion"], col["consumoSPA"]]).size().unstack().plot(
        kind="bar", stacked=True, figsize=(12, 6)
    )
    plt.title("Consumo de SPA según la relación víctima–agresor")
    plt.ylabel("Cantidad")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/graficas_spa/spa_relacion.png")
    plt.close()

    # =====================================================
    # G5 — Heatmap: Consumo SPA × Mecanismo de agresión
    # =====================================================
    tabla_heatmap = df.pivot_table(
        index=col["consumoSPA"],
        columns=col["mecanismo"],
        values=col["edad"],
        aggfunc="count",
        fill_value=0
    )

    plt.figure(figsize=(12, 7))
    plt.imshow(tabla_heatmap, cmap="Purples")
    plt.colorbar(label="Cantidad de casos")
    plt.xticks(range(len(tabla_heatmap.columns)), tabla_heatmap.columns, rotation=45)
    plt.yticks(range(len(tabla_heatmap.index)), tabla_heatmap.index)
    plt.title("Heatmap: Consumo SPA vs Mecanismo de agresión")
    plt.tight_layout()
    plt.savefig("static/graficas_spa/heatmap_spa_mecanismo.png")
    plt.close()

    # =====================================================
    # G6 — Rango de edad × Consumo de SPA
    # =====================================================
    plt.figure(figsize=(12, 6))
    df.groupby(["edad_rango", col["consumoSPA"]]).size().unstack().plot(
        kind="bar", figsize=(12, 6)
    )
    plt.title("Consumo de SPA según rango de edad")
    plt.ylabel("Cantidad")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/graficas_spa/spa_edad_rangos.png")
    plt.close()

    # =====================================================
    # RETORNAR HTML
    # =====================================================
    return render_template(
        "HI-SPA.html",
        g1="graficas_spa/spa_distrib.png",
        g2="graficas_spa/alcohol_distrib.png",
        g3="graficas_spa/spa_sexo_victima.png",
        g4="graficas_spa/spa_relacion.png",
        g5="graficas_spa/heatmap_spa_mecanismo.png",
        g6="graficas_spa/spa_edad_rangos.png",
        tabla=tabla_json,
        columnas=columnas_mostrar
    )



