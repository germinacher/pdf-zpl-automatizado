

import os
from pdf2image import convert_from_path
from zplgrf import GRF

def pdf_to_zpl(pdf_path, output_path, dpi=203, device_width=None, width_adjustment_cm=1.0, left_offset_cm=1.5, scale_factor=0.7, top_offset_cm=0.3, poppler_path=None):
    # Convertir PDF a imágenes (solo la primera página)
    if poppler_path is None:
        poppler_path = os.environ.get("POPPLER_PATH")
    pages = convert_from_path(pdf_path, dpi=dpi, poppler_path=poppler_path)
    img = pages[0]
    
    # Redimensionar la imagen si se especifica un factor de escala
    if scale_factor != 1.0:
        from PIL import Image
        new_width = int(img.width * scale_factor)
        new_height = int(img.height * scale_factor)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        print(f"[INFO] Imagen redimensionada: {img.width}x{img.height}px (factor: {scale_factor})")
    
    # Calcular el ancho del dispositivo y el desplazamiento hacia la izquierda
    if device_width is None:
        # Convertir centímetros a píxeles
        left_offset_pixels = int(left_offset_cm * dpi / 2.54)  # Desplazamiento hacia la izquierda
        width_adjustment_pixels = int(width_adjustment_cm * dpi / 2.54)  # Ajuste de ancho
        
        # El ancho del dispositivo debe ser el ancho de la imagen + el desplazamiento + el ajuste
        device_width = img.width + left_offset_pixels + width_adjustment_pixels
        print(f"[INFO] Ancho de imagen: {img.width}px")
        print(f"[INFO] Desplazamiento izquierda: -{left_offset_pixels}px ({left_offset_cm}cm)")
        print(f"[INFO] Ajuste ancho: +{width_adjustment_pixels}px ({width_adjustment_cm}cm)")
        print(f"[INFO] Ancho total dispositivo: {device_width}px")

    # Guardar temporalmente como PNG
    temp_img = pdf_path.replace(".pdf", ".png")
    img.save(temp_img, "PNG")

    # Convertir PNG a ZPL usando zplgrf
    # Crear un nombre de archivo GRF válido (1-8 caracteres alfanuméricos)
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    sanitized = ''.join(ch for ch in base_name if ch.isalnum()).upper()[:8] or 'IMAGE'
    
    with open(temp_img, "rb") as f:
        grf = GRF.from_image(f.read(), filename=sanitized)
        zpl = grf.to_zpl()
        
        # Si hay desplazamiento, modificar el ZPL
        if left_offset_cm > 0 or top_offset_cm > 0:
            left_offset_pixels = int(left_offset_cm * dpi / 2.54)
            top_offset_pixels = int(top_offset_cm * dpi / 2.54)
            import re
            # En lugar de usar coordenadas negativas, vamos a usar un enfoque diferente
            # Agregar un comando ^FO antes del comando ^GF para posicionar la imagen
            # Buscar el patrón ^XA seguido de cualquier cosa hasta ^GF y agregar ^FO antes
            zpl = re.sub(r'(\^XA.*?)(\^GF)', f'\\1^FO{left_offset_pixels},{top_offset_pixels}\\2', zpl, flags=re.DOTALL)
            print(f"[INFO] Aplicando desplazamiento horizontal: {left_offset_pixels}px, vertical: {top_offset_pixels}px")
            print(f"[INFO] Comando ZPL modificado: ^FO{left_offset_pixels},{top_offset_pixels}")

    # Guardar ZPL
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(zpl)

    # Borrar temporal
    os.remove(temp_img)
    
    return zpl

def pdf_to_zpl_content(pdf_path, dpi=203, device_width=None, width_adjustment_cm=1.0, left_offset_cm=1.5, scale_factor=0.7, top_offset_cm=0.3, poppler_path=None):
    # Convertir PDF a imágenes (solo la primera página)
    if poppler_path is None:
        poppler_path = os.environ.get("POPPLER_PATH")
    pages = convert_from_path(pdf_path, dpi=dpi, poppler_path=poppler_path)
    img = pages[0]
    
    # Redimensionar la imagen si se especifica un factor de escala
    if scale_factor != 1.0:
        from PIL import Image
        new_width = int(img.width * scale_factor)
        new_height = int(img.height * scale_factor)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        print(f"[INFO] Imagen redimensionada: {img.width}x{img.height}px (factor: {scale_factor})")
    
    # Calcular el ancho del dispositivo y el desplazamiento hacia la izquierda
    if device_width is None:
        # Convertir centímetros a píxeles
        left_offset_pixels = int(left_offset_cm * dpi / 2.54)  # Desplazamiento hacia la izquierda
        width_adjustment_pixels = int(width_adjustment_cm * dpi / 2.54)  # Ajuste de ancho
        
        # El ancho del dispositivo debe ser el ancho de la imagen + el desplazamiento + el ajuste
        device_width = img.width + left_offset_pixels + width_adjustment_pixels
        print(f"[INFO] Ancho de imagen: {img.width}px")
        print(f"[INFO] Desplazamiento izquierda: -{left_offset_pixels}px ({left_offset_cm}cm)")
        print(f"[INFO] Ajuste ancho: +{width_adjustment_pixels}px ({width_adjustment_cm}cm)")
        print(f"[INFO] Ancho total dispositivo: {device_width}px")

    # Guardar temporalmente como PNG
    temp_img = pdf_path.replace(".pdf", ".png")
    img.save(temp_img, "PNG")

    # Convertir PNG a ZPL usando zplgrf
    # Crear un nombre de archivo GRF válido (1-8 caracteres alfanuméricos)
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    sanitized = ''.join(ch for ch in base_name if ch.isalnum()).upper()[:8] or 'IMAGE'
    
    with open(temp_img, "rb") as f:
        grf = GRF.from_image(f.read(), filename=sanitized)
        zpl = grf.to_zpl()
        
        # Si hay desplazamiento, modificar el ZPL
        if left_offset_cm > 0 or top_offset_cm > 0:
            left_offset_pixels = int(left_offset_cm * dpi / 2.54)
            top_offset_pixels = int(top_offset_cm * dpi / 2.54)
            import re
            # En lugar de usar coordenadas negativas, vamos a usar un enfoque diferente
            # Agregar un comando ^FO antes del comando ^GF para posicionar la imagen
            # Buscar el patrón ^XA seguido de cualquier cosa hasta ^GF y agregar ^FO antes
            zpl = re.sub(r'(\^XA.*?)(\^GF)', f'\\1^FO{left_offset_pixels},{top_offset_pixels}\\2', zpl, flags=re.DOTALL)
            print(f"[INFO] Aplicando desplazamiento horizontal: {left_offset_pixels}px, vertical: {top_offset_pixels}px")
            print(f"[INFO] Comando ZPL modificado: ^FO{left_offset_pixels},{top_offset_pixels}")

    # Borrar temporal
    os.remove(temp_img)
    
    return zpl

def procesar_pdfs(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    
    # Lista para almacenar todos los comandos ZPL
    todos_zpl = []
    
    # Procesar todos los PDFs
    pdfs = [f for f in os.listdir(input_folder) if f.lower().endswith(".pdf")]
    
    for i, archivo in enumerate(pdfs):
        pdf_path = os.path.join(input_folder, archivo)
        print(f"[INFO] Procesando {archivo}...")
        
        # Generar ZPL para este PDF (sin guardar archivo individual)
        zpl_content = pdf_to_zpl_content(pdf_path)
        todos_zpl.append(zpl_content)
        print(f"[OK] Procesado: {archivo}")
    
    # Combinar todos los ZPL en un solo archivo
    if todos_zpl:
        archivo_combinado = os.path.join(output_folder, "todas_las_etiquetas.zpl")
        with open(archivo_combinado, "w", encoding="utf-8") as f:
            for zpl in todos_zpl:
                f.write(zpl)
                f.write("\n")  # Separador entre etiquetas
        
        print(f"[OK] Archivo combinado generado: {archivo_combinado}")
        print(f"[INFO] Total de etiquetas procesadas: {len(todos_zpl)}")
    else:
        print("[INFO] No se encontraron archivos PDF para procesar")

if __name__ == "__main__":
    procesar_pdfs("entrada", "salida")
