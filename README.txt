Automatización con python para convertir PDF a ZPL (Imagen con ^GFA).

Este script convierte automaticamente archivos PDF en código ZPL usando imágenes GFA.

Convierte el PDF entero en una imagen y la traduce a código GFA (Zebra Graphic Field ASCII).
Esto significa que la impresora recibe la etiqueta como una imagen rasterizada, no como texto vectorial.

Requisitos
1. Tener Python 3 instalado.

2. Crear nuevo entorno virtual con el comando: python -m venv env

Instalar dependencias: (o utilizar requirements.txt)
   pip install pdf2image pillow zplgrf
   pip install pdfplumber
   
3. Instalar Poppler en tu sistema (necesario para pdf2image).
   - Windows: https://github.com/oschwartz10612/poppler-windows/releases/
   - Agregar directorio de carpeta bin al PATH

4. Ejecutar entorno virtual en el simbolo del sistema, estando en el directorio del programa poner:
   env\Scripts\activate

Uso
0. Borra los archivos .txt de las carpetas de "entrada" y "salida". Los llamados .gitkeep.
1. Copia tus archivos PDF en la carpeta "entrada".
2. Ejecuta el script:
   python main.py 
3. Los archivos `.zpl` estarán en la carpeta "salida".

Notas
- Solo procesa la primera página de cada PDF.
- Puedes ajustar `dpi` y `device_width` en `main.py` para cambiar la calidad/tamaño.
- El resultado es un archivo ZPL con un objeto gráfico `^GFA`, que replica exactamente el PDF como imagen.

Como funciona el programa?
1- Convierte todos los PDF a una imagen usando pdf2image (cada primer página de cada PDF se transforma en una imagen .png temporal).
2- Usa la clase GRF del módulo zplgrf, que sirve para convertir imágenes en formato Zebra Graphic Field (GFA).
3- Por tanto, el resultado ZPL que genera el script contiene bloques como ~DGR o ^GF, que son los comandos usados para imprimir imágenes en formato GFA.
