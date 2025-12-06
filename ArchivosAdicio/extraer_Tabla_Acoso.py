import pdfplumber
import pandas as pd
import re


def convertir_decimal(col):
    return col.apply(
        lambda x: float(x.replace(",", ".")) if isinstance(x, str) and re.match(r"^\d+,\d+$", x) else x
    )


def limpiar_tabla(df):
    # Quitar filas vacías
    df = df.dropna(how='all')

    # Primera fila → encabezados reales
    df.columns = [
        re.sub(r"\n", " ", str(c)).strip().lower().replace("  ", " ")
        for c in df.iloc[0]
    ]

    # Quitar fila del encabezado
    df = df[1:].reset_index(drop=True)

    # Convertir decimales donde aplique
    for col in df.columns:
        df[col] = convertir_decimal(df[col])

    return df



def extraer_tablas_pdf(ruta_pdf):
    tablas_limpias = []

    with pdfplumber.open(ruta_pdf) as pdf:
        for page in pdf.pages:
            tablas = page.extract_tables()

            for tabla in tablas:
                try:
                    df = pd.DataFrame(tabla)
                    df = limpiar_tabla(df)
                    tablas_limpias.append(df)
                except Exception as e:
                    print("No se pudo procesar tabla:", e)

    return tablas_limpias


if __name__ == "__main__":
    archivo = "acoso.pdf"

    print("\n📌 Extrayendo tablas del PDF...\n")
    tablas = extraer_tablas_pdf(archivo)

    for i, df in enumerate(tablas):
        print(f"\n============================")
        print(f" TABLA {i+1} LIMPIA ")
        print("============================\n")
        print(df)

        # Guardar tabla como Excel
        nombre_archivo = f"tabla_acoso_{i+1}.xlsx"
        df.to_excel(nombre_archivo, index=False)
        print(f"✔ Guardada: {nombre_archivo}")

    print("\n✔ Proceso completado. Tablas guardadas en formato XLSX.")
