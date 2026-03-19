import pandas as pd
import re


def read_dispatch_excel(file_path, fecha):
    raw = pd.read_excel(file_path, header=None, engine="openpyxl")

    header_rows = raw.iloc[3:6].fillna("")

    columns = []
    for col in range(raw.shape[1]):
        parts = header_rows.iloc[:, col].astype(str).str.strip()
        col_name = " ".join([p for p in parts if p])
        columns.append(col_name)

    df = raw.iloc[6:].copy()
    df.columns = columns

    try:
        col_hora = [c for c in df.columns if "Día Hora" in c][0]
        col_charcani = [c for c in df.columns if "CHARCANI V" in c][0]
        col_cmg = [c for c in df.columns if "Socabaya" in c][0]
    except IndexError:
        raise ValueError("Columnas no encontradas")

    df = df[[col_hora, col_charcani, col_cmg]].copy()
    df.columns = ["hora", "charcani_v", "cmg_socabaya"]

    df["hora"] = df["hora"].astype(str).str.strip()
    df = df[df["hora"].str.match(r"^\d{2}:\d{2}$", na=False)]

    df["charcani_v"] = pd.to_numeric(df["charcani_v"], errors="coerce")
    df["cmg_socabaya"] = pd.to_numeric(df["cmg_socabaya"], errors="coerce")

    df["datetime"] = pd.to_datetime(
        fecha.strftime("%Y-%m-%d") + " " + df["hora"],
        format="%Y-%m-%d %H:%M",
    )

    return df.sort_values("datetime").reset_index(drop=True)