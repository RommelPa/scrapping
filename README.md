# COES Scraper

Pipeline para extracción, procesamiento incremental y almacenamiento de datos de despacho eléctrico desde COES.

## Features

- Scraping automático
- Detección de cambios por hash
- Procesamiento incremental
- Validación de datos
- Almacenamiento en SQLite

## Estructura

src/
- scraper.py
- downloader.py
- parser.py
- merge.py
- validator.py
- db.py

## Uso

```bash
python main.py
```

## Output

Datos almacenados en:

```bash
data/coes.db
```
## 1. Clonar repositorio (SSH)

```bash
git clone git@github.com:RommelPa/scrapping.git
```

```bash
cd scrapping
```

## 2. Crear entorno virtual

```bash
python -m venv .venv
```

```bash
.venv\Scripts\activate
```

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 4. Estructura necesaria

```bash
mkdir data\raw
```

## 5. Ejecutar

```bash
python main.py
```