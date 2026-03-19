def validar_outliers(df):
    errores = []

    # ---- CHARCANI ----
    if (df["charcani_v"] < 0).any():
        errores.append("charcani_v tiene valores negativos")

    if (df["charcani_v"] > 500).any():
        errores.append("charcani_v fuera de rango (>500)")

    # ---- CMG ----
    if (df["cmg_socabaya"] < 0).any():
        errores.append("cmg_socabaya negativo")

    if (df["cmg_socabaya"] > 200).any():
        errores.append("cmg_socabaya fuera de rango (>200)")

    # ---- NULOS ----
    if df[["charcani_v", "cmg_socabaya"]].isnull().any().any():
        errores.append("hay valores nulos")

    if errores:
        raise ValueError(" | ".join(errores))

    return True