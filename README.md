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

## 1. Generar clave SSH

```bash
ssh-keygen -t ed25519 -C "tu_email@ejemplo.com"
```

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

```bash
cat ~/.ssh/id_ed25519.pub
```

Ve a GitHub → Settings → SSH and GPG keys → New SSH key y copia el contenido

## 2. Clonar repositorio (SSH)

```bash
git clone git@github.com:RommelPa/scrapping.git
```

```bash
cd scrapping
```

## 3. Crear entorno virtual

```bash
python -m venv .venv
```

```bash
.venv\Scripts\activate
```

## 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 5. Estructura necesaria

```bash
mkdir data\raw
```

## 5. Ejecutar

```bash
python main.py
```

## Output

Datos almacenados en:

```bash
data/coes.db
```