import os
import requests
from src.scraper import session

URL_DOWNLOAD = "https://www.coes.org.pe/Portal/browser/download"


def descargar_archivo(ruta_archivo: str, destino: str):
    url = f"{URL_DOWNLOAD}?url={requests.utils.quote(ruta_archivo, safe='/')}"

    with session.get(url, stream=True) as r:
        r.raise_for_status()

        with open(destino, "wb") as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)