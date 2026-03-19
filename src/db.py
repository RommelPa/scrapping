import sqlite3
from pathlib import Path
import pandas as pd
import hashlib

DB_PATH = Path("data/coes.db")


# ---------------- CONEXIÓN ----------------
def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


# ---------------- INIT DB ----------------
def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dispatch_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            datetime TEXT NOT NULL,
            hora TEXT NOT NULL,
            charcani_v REAL,
            cmg_socabaya REAL,
            fuente TEXT NOT NULL,
            UNIQUE(datetime, fuente)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS processed_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            nombre_archivo TEXT NOT NULL,
            tipo TEXT NOT NULL,
            hash TEXT NOT NULL,
            procesado_en TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(nombre_archivo, fecha)
        )
        """)

        conn.commit()


# ---------------- HASH ----------------
def calcular_hash_archivo(path):
    hash_sha256 = hashlib.sha256()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_sha256.update(chunk)

    return hash_sha256.hexdigest()


# ---------------- CAMBIO REAL ----------------
def archivo_cambio(nombre_archivo: str, hash_actual: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT hash FROM processed_files
            WHERE nombre_archivo = ?
        """, (nombre_archivo,))

        row = cursor.fetchone()

        if row is None:
            return True  # nuevo archivo

        return row[0] != hash_actual


# ---------------- MARCAR PROCESADO ----------------
def marcar_archivo_procesado(nombre_archivo: str, fecha: str, tipo: str, hash_val: str):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO processed_files
            (nombre_archivo, fecha, tipo, hash)
            VALUES (?, ?, ?, ?)
        """, (nombre_archivo, fecha, tipo, hash_val))

        conn.commit()


# ---------------- GUARDAR DATA ----------------
def guardar_dataframe(df, fecha: str, fuente: str):
    with get_connection() as conn:
        cursor = conn.cursor()

        rows = [
            (
                fecha,
                row["datetime"].isoformat(),
                row["hora"],
                row["charcani_v"],
                row["cmg_socabaya"],
                fuente
            )
            for _, row in df.iterrows()
        ]

        cursor.executemany("""
            INSERT OR REPLACE INTO dispatch_data
            (fecha, datetime, hora, charcani_v, cmg_socabaya, fuente)
            VALUES (?, ?, ?, ?, ?, ?)
        """, rows)

        conn.commit()


# ---------------- CARGAR DESDE DB ----------------
def cargar_datos_por_fecha(fecha: str):
    with get_connection() as conn:
        query = """
        SELECT datetime, hora, charcani_v, cmg_socabaya
        FROM dispatch_data
        WHERE fecha = ? AND fuente = 'final'
        ORDER BY datetime
        """

        df = pd.read_sql_query(query, conn, params=(fecha,))

    if df.empty:
        return df

    df["datetime"] = pd.to_datetime(df["datetime"])
    return df