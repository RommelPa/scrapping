import requests
from bs4 import BeautifulSoup

URL_VISTADATOS = "https://www.coes.org.pe/Portal/browser/vistadatos"


def crear_sesion():
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest",
    })
    s.get("https://www.coes.org.pe/Portal/Operacion/ProgOperacion/ProgramaDiario")
    return s


session = crear_sesion()

MESES = {
    1: "01_ENERO",
    2: "02_FEBRERO",
    3: "03_MARZO",
    4: "04_ABRIL",
    5: "05_MAYO",
    6: "06_JUNIO",
    7: "07_JULIO",
    8: "08_AGOSTO",
    9: "09_SETIEMBRE",
    10: "10_OCTUBRE",
    11: "11_NOVIEMBRE",
    12: "12_DICIEMBRE",
}

BASE_PROGRAMA = "Operación/Programa de Operación/Programa Diario/"
BASE_REPROG = "Operación/Programa de Operación/Reprograma Diario Operación/"


def listar_directorio(base_dir: str, ruta: str, initial: str):
    data = {
        "baseDirectory": base_dir,
        "url": ruta,
        "indicador": "S",
        "initialLink": initial,
        "orderFolder": "D",
    }

    r = session.post(URL_VISTADATOS, data=data)
    r.raise_for_status()

    return BeautifulSoup(r.text, "html.parser")


def build_ruta(base, fecha):
    anio = fecha.strftime("%Y")
    mes = MESES[fecha.month]
    dia = f"Día {int(fecha.strftime('%d'))}"

    return f"{base}{anio}/{mes}/{dia}/"


def extraer_nombres(soup):
    nombres = []

    # tablas
    for tr in soup.select("tr.selector-file-contextual"):
        celdas = tr.find_all("td")
        if len(celdas) >= 3:
            nombres.append(celdas[2].text.strip())

    # listas
    for a in soup.select("a.infolist-link"):
        nombres.append(a.text.strip())

    return list(set(nombres))


# ---------------- PROGRAMA ----------------

def obtener_programa(fecha):
    ruta = build_ruta(BASE_PROGRAMA, fecha)

    soup = listar_directorio(
        BASE_PROGRAMA,
        ruta,
        "Programa de Operación Diario"
    )

    for tr in soup.select("tr.selector-file-contextual"):
        celdas = tr.find_all("td")

        if len(celdas) < 3:
            continue

        nombre = celdas[2].text.strip()

        if nombre.startswith("Anexo1_Despacho"):
            return {
                "ruta": tr.get("id"),
                "nombre": nombre
            }

    return None


# ---------------- REPROGRAMAS ----------------

def obtener_reprogramas(fecha):
    ruta_base = build_ruta(BASE_REPROG, fecha)

    soup = listar_directorio(
        BASE_REPROG,
        ruta_base,
        "Reprograma Diario de Operación"
    )

    carpetas = [n for n in extraer_nombres(soup) if "Reprog" in n]
    carpetas = sorted(carpetas)

    archivos = []

    for carpeta in carpetas:
        ruta = f"{ruta_base}{carpeta}/"

        soup_sub = listar_directorio(
            BASE_REPROG,
            ruta,
            "Reprograma Diario de Operación"
        )

        for tr in soup_sub.select("tr.selector-file-contextual"):
            celdas = tr.find_all("td")

            if len(celdas) < 3:
                continue

            nombre = celdas[2].text.strip()

            if nombre.startswith("Reprog_") and nombre.endswith(".xlsx"):
                archivos.append({
                    "ruta": tr.get("id"),
                    "nombre": nombre
                })

    return archivos