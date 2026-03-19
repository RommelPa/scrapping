def merge_reprograma(df_base, df_reprog):
    if df_base["datetime"].duplicated().any():
        raise ValueError("Duplicados en base")

    if df_reprog["datetime"].duplicated().any():
        raise ValueError("Duplicados en reprog")

    df_result = df_base.set_index("datetime")
    df_reprog = df_reprog.set_index("datetime")

    df_result.update(df_reprog)

    df_result = df_result.reset_index()

    if df_result["datetime"].duplicated().any():
        raise ValueError("Duplicados después del merge")

    return df_result