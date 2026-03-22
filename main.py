from datetime import datetime
import os
import re

from src.scraper import obtener_programa, obtener_reprogramas
from src.downloader import descargar_archivo
from src.parser import read_dispatch_excel
from src.merge import merge_reprograma
from src.validator import validar_outliers

from src.db import (
    init_db,
    calcular_hash_archivo,
    archivo_cambio,
    marcar_archivo_procesado,
    guardar_dataframe,
    cargar_datos_por_fecha
)

def ordenar_reprog(nombre):
    match = re.search(r"Reprog_\d+([A-Z])", nombre)
    return match.group(1) if match else ""

def main():
    init_db()
    fecha = datetime(2026, 3, 22)

    os.makedirs("data/raw", exist_ok=True)

    hubo_cambios = False

    # ================= PROGRAMA =================
    prog = obtener_programa(fecha)
    if not prog:
        print("No se encontró programa diario (posible demora de COES)")
        return

    path_prog = f"data/raw/{prog['nombre']}"
    descargar_archivo(prog["ruta"], path_prog)

    hash_prog = calcular_hash_archivo(path_prog)

    if archivo_cambio(prog["nombre"], hash_prog):
        print("Programa nuevo o modificado")

        df = read_dispatch_excel(path_prog, fecha)

        marcar_archivo_procesado(
            prog["nombre"],
            fecha.strftime("%Y-%m-%d"),
            "programa",
            hash_prog
        )

        hubo_cambios = True
    else:
        print("Programa sin cambios")

        df = cargar_datos_por_fecha(fecha.strftime("%Y-%m-%d"))

        if df is None or df.empty:
            print("No hay datos previos en DB para esta fecha")
            return

    # ================= REPROGRAMAS =================
    try:
        reprogs = obtener_reprogramas(fecha)
    except Exception as e:
        print(f"[ERROR] Fallo al obtener reprogramas: {e}")
        reprogs = []

    reprogs = sorted(reprogs, key=lambda x: ordenar_reprog(x["nombre"]))

    print(f"Reprogramas encontrados: {len(reprogs)}")

    for r in reprogs:
        path = f"data/raw/{r['nombre']}"
        descargar_archivo(r["ruta"], path)

        hash_r = calcular_hash_archivo(path)

        if not archivo_cambio(r["nombre"], hash_r):
            print(f"Sin cambios: {r['nombre']}")
            continue

        print(f"Procesando: {r['nombre']}")

        try:
            df_r = read_dispatch_excel(path, fecha)
            df = merge_reprograma(df, df_r)

            marcar_archivo_procesado(
                r["nombre"],
                fecha.strftime("%Y-%m-%d"),
                "reprograma",
                hash_r
            )

            hubo_cambios = True

        except Exception as e:
            print(f"Error en {r['nombre']}: {e}")

    # ================= GUARDADO =================
    if hubo_cambios:
        validar_outliers(df)

        guardar_dataframe(
            df,
            fecha.strftime("%Y-%m-%d"),
            "final"
        )

        print("\nDatos actualizados en SQLite")
    else:
        print("\nSin cambios, no se actualiza la base")

    print(df.head())


if __name__ == "__main__":
    main()