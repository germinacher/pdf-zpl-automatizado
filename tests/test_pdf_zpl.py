import os
import re
import pytest
from unittest.mock import patch, MagicMock, mock_open


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_fake_image(width=400, height=600):
    """Devuelve un Mock que simula una imagen PIL."""
    img = MagicMock()
    img.width = width
    img.height = height
    img.resize.return_value = img
    return img


SAMPLE_ZPL = "^XA^GFA,100,100,10,:Z64:abc==^FS^XZ"


# ---------------------------------------------------------------------------
# pdf_to_zpl_content
# ---------------------------------------------------------------------------

class TestPdfToZplContent:

    @patch("main.GRF")
    @patch("main.convert_from_path")
    def test_retorna_string_zpl(self, mock_convert, mock_grf):
        """La función debe devolver un string que contenga comandos ZPL."""
        mock_convert.return_value = [make_fake_image()]
        grf_instance = MagicMock()
        grf_instance.to_zpl.return_value = SAMPLE_ZPL
        mock_grf.from_image.return_value = grf_instance

        from main import pdf_to_zpl_content

        with patch("builtins.open", mock_open(read_data=b"fake_png")):
            with patch("os.remove"):
                result = pdf_to_zpl_content("fake.pdf")

        assert isinstance(result, str)
        assert "^XA" in result
        assert "^XZ" in result

    @patch("main.GRF")
    @patch("main.convert_from_path")
    def test_aplica_escala(self, mock_convert, mock_grf):
        """Con scale_factor != 1.0 debe llamarse a img.resize."""
        img = make_fake_image(400, 600)
        mock_convert.return_value = [img]
        grf_instance = MagicMock()
        grf_instance.to_zpl.return_value = SAMPLE_ZPL
        mock_grf.from_image.return_value = grf_instance

        from main import pdf_to_zpl_content

        with patch("builtins.open", mock_open(read_data=b"fake_png")):
            with patch("os.remove"):
                pdf_to_zpl_content("fake.pdf", scale_factor=0.5)

        img.resize.assert_called_once()
        args = img.resize.call_args[0][0]  # (new_width, new_height)
        assert args == (200, 300)

    @patch("main.GRF")
    @patch("main.convert_from_path")
    def test_sin_escala_no_llama_resize(self, mock_convert, mock_grf):
        """Con scale_factor=1.0 no debe redimensionarse la imagen."""
        img = make_fake_image()
        mock_convert.return_value = [img]
        grf_instance = MagicMock()
        grf_instance.to_zpl.return_value = SAMPLE_ZPL
        mock_grf.from_image.return_value = grf_instance

        from main import pdf_to_zpl_content

        with patch("builtins.open", mock_open(read_data=b"fake_png")):
            with patch("os.remove"):
                pdf_to_zpl_content("fake.pdf", scale_factor=1.0)

        img.resize.assert_not_called()

    @patch("main.GRF")
    @patch("main.convert_from_path")
    def test_offset_agrega_fo(self, mock_convert, mock_grf):
        """Con offsets > 0 el ZPL debe incluir el comando ^FO."""
        mock_convert.return_value = [make_fake_image()]
        grf_instance = MagicMock()
        grf_instance.to_zpl.return_value = SAMPLE_ZPL
        mock_grf.from_image.return_value = grf_instance

        from main import pdf_to_zpl_content

        with patch("builtins.open", mock_open(read_data=b"fake_png")):
            with patch("os.remove"):
                result = pdf_to_zpl_content(
                    "fake.pdf",
                    left_offset_cm=1.5,
                    top_offset_cm=0.3,
                    scale_factor=1.0,
                )

        assert "^FO" in result

    @patch("main.GRF")
    @patch("main.convert_from_path")
    def test_sin_offset_no_agrega_fo(self, mock_convert, mock_grf):
        """Con offsets en 0 el ZPL no debe incluir ^FO."""
        mock_convert.return_value = [make_fake_image()]
        grf_instance = MagicMock()
        grf_instance.to_zpl.return_value = SAMPLE_ZPL
        mock_grf.from_image.return_value = grf_instance

        from main import pdf_to_zpl_content

        with patch("builtins.open", mock_open(read_data=b"fake_png")):
            with patch("os.remove"):
                result = pdf_to_zpl_content(
                    "fake.pdf",
                    left_offset_cm=0,
                    top_offset_cm=0,
                    scale_factor=1.0,
                )

        assert "^FO" not in result


# ---------------------------------------------------------------------------
# procesar_pdfs
# ---------------------------------------------------------------------------

class TestProcesarPdfs:

    @patch("main.pdf_to_zpl_content")
    @patch("os.listdir")
    @patch("os.makedirs")
    def test_genera_archivo_combinado(self, mock_makedirs, mock_listdir, mock_content):
        """Debe crear 'todas_las_etiquetas.zpl' con el ZPL de cada PDF."""
        mock_listdir.return_value = ["a.pdf", "b.pdf"]
        mock_content.return_value = SAMPLE_ZPL

        from main import procesar_pdfs

        m = mock_open()
        with patch("builtins.open", m):
            procesar_pdfs("entrada", "salida")

        assert mock_content.call_count == 2

        handle = m()
        written = "".join(call.args[0] for call in handle.write.call_args_list)
        assert SAMPLE_ZPL in written

    @patch("main.pdf_to_zpl_content")
    @patch("os.listdir")
    @patch("os.makedirs")
    def test_sin_pdfs_no_escribe(self, mock_makedirs, mock_listdir, mock_content):
        """Si no hay PDFs, no debe llamarse a pdf_to_zpl_content ni escribirse nada."""
        mock_listdir.return_value = ["archivo.txt", "imagen.jpg"]

        from main import procesar_pdfs

        with patch("builtins.open", mock_open()):
            procesar_pdfs("entrada", "salida")

        mock_content.assert_not_called()

    @patch("main.pdf_to_zpl_content")
    @patch("os.listdir")
    @patch("os.makedirs")
    def test_ignora_archivos_no_pdf(self, mock_makedirs, mock_listdir, mock_content):
        """Solo debe procesar archivos .pdf, ignorando el resto."""
        mock_listdir.return_value = ["etiqueta.pdf", "notas.txt", "foto.png"]
        mock_content.return_value = SAMPLE_ZPL

        from main import procesar_pdfs

        with patch("builtins.open", mock_open()):
            procesar_pdfs("entrada", "salida")

        assert mock_content.call_count == 1