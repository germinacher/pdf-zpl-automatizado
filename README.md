# 📄 Automatización en Python: Conversión de PDF a ZPL (GFA)

Este proyecto automatiza la **conversión de múltiples archivos PDF a ZPL**, generando etiquetas listas para imprimir en impresoras Zebra mediante **imágenes GFA (`^GFA`)**.

El script convierte **la primera página de cada PDF** en una imagen y la traduce automáticamente a código ZPL, permitiendo imprimir **muchas etiquetas con un solo comando**.

---

## 🧠 ¿Cómo funciona?

1. Convierte la **primera página de cada PDF** en una imagen (`.png`) usando `pdf2image`.
2. Transforma esa imagen en código **Zebra Graphic Field ASCII (GFA)** utilizando `zplgrf`.
3. Genera un archivo **ZPL** que contiene comandos como `^GF` / `~DGR`, los cuales permiten a la impresora renderizar la etiqueta como una **imagen rasterizada**.

📌 La impresora **no recibe texto vectorial**, sino una réplica exacta del PDF como imagen, garantizando fidelidad visual.

---

## 🚀 Características principales

- Procesa **múltiples PDFs automáticamente**
- Convierte PDFs a **archivos ZPL**
- Flujo optimizado para **impresión masiva**
- Ideal para entornos de **logística y e-commerce**
- Ejecutable con **un solo comando**

---

## 📦 Requisitos

### 1️⃣ Python
- Python **3.x** instalado

### 2️⃣ Entorno virtual
```bash
python -m venv env
```

 Activar el entorno virtual (Windows):

```bash
env\Scripts\activate
```

### 3️⃣ Dependencias
Instalar manualmente:
```bash
pip install pdf2image pillow zplgrf pdfplumber
```

O usando `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4️⃣ Poppler (requerido por pdf2image)

- Descargar desde: https://github.com/oschwartz10612/poppler-windows/releases/

- Agregar la carpeta `bin` de Poppler al **PATH** del sistema

### ▶️ Uso

### 0️⃣ Elimina los archivos `.txt` de las carpetas `entrada` y `salida` (archivos `.gitkeep`).

### 1️⃣ Copia los archivos **PDF** en la carpeta:
```bash
entrada/
```

### 2️⃣ Ejecuta el script:
```bash
python main.py
```

### 3️⃣ Los archivos `.zpl` **generados** estarán disponibles en:
```bash
salida/
```

## ⚙️ Configuración

Puedes ajustar los siguientes parámetros en `main.py`:
- `dpi`: controla la calidad de la imagen generada
- `device_width`: ajusta el ancho de la etiqueta según la impresora

## 📝 Notas importantes

- El script **solo procesa la primera página** de cada PDF
- El ZPL generado contiene objetos gráficos `^GFA`
- El resultado es una **réplica exacta del PDF**, ideal para etiquetas complejas

## 📈 Caso de uso real

Esta automatización fue diseñada para optimizar la impresión de etiquetas en un entorno de e-commerce con alto volumen, reduciendo drásticamente el tiempo de procesamiento y eliminando pasos manuales repetitivos.
