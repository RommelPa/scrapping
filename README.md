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