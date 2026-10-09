import re
import uuid
from pathlib import Path
from fpdf import FPDF
from PIL import Image

# Point BASE_DIR directly to the app directory containing static/
APP_DIR = Path(__file__).resolve().parent.parent
EXPORT_DIR = APP_DIR / "static" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
_MAP = {"•": "-", "—": "-", "–": "-", "‘": "'", "’": "'",
        "“": '"', "”": '"', "…": "...", "\u00a0": " "}

def _t(s) -> str:
    s = str(s)
    for k, v in _MAP.items():
        s = s.replace(k, v)
    return s.encode("latin-1", "replace").decode("latin-1")

def _get_local_image_path(web_path: str) -> Path:
    clean_path = web_path.lstrip("/")
    # Handle both '/static/...' and 'static/...' paths relative to app/
    if clean_path.startswith("static/"):
        return APP_DIR / clean_path
    return APP_DIR / "static" / clean_path


def save_pdf(comic: dict) -> str:
    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=False)

    for panel in comic["panels"]:
        pdf.add_page()
        pdf.set_fill_color(20, 20, 30)
        pdf.rect(0, 0, 297, 210, "F")

        # Title
        pdf.set_text_color(255, 214, 82)
        pdf.set_font("Helvetica", "B", 24)
        pdf.set_xy(14, 10)
        pdf.cell(0, 12, _t(comic.get("title", "ComicCraft"))[:45])

        # Panel subheader
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_xy(14, 25)
        pdf.cell(0, 9, _t(f"PANEL {panel.get('number', 1)} - {panel.get('title', '')}")[:70])

        # Draw Panel Image
        image_path = _get_local_image_path(panel.get("image", ""))
        if image_path.exists():
            try:
                with Image.open(image_path) as img:
                    w, h = img.size
                    ratio = w / h if h > 0 else 1.77
                    box_w, box_h = 265, 115
                    if ratio > (box_w / box_h):
                        box_h = box_w / ratio
                    else:
                        box_w = box_h * ratio
                pdf.image(str(image_path), x=16, y=39, w=box_w, h=box_h)
            except Exception as e:
                print(f"Error embedding image in PDF: {e}")
        else:
            print(f"PDF Exporter image not found at: {image_path}")

        # Text Captions & Narration
        text_y = 39 + 115 + 4
        pdf.set_text_color(255, 214, 82)
        pdf.set_font("Helvetica", "I", 10)
        pdf.set_xy(16, text_y)
        pdf.multi_cell(265, 5, _t(panel.get("caption", ""))[:180])

        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "", 11)
        pdf.set_xy(16, text_y + 9)
        pdf.multi_cell(265, 5, _t(panel.get("narration", ""))[:500])

        if panel.get("dialogue"):
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_xy(16, 193)
            pdf.cell(265, 7, _t(f'"{panel.get("dialogue")}"')[:150], align="C")

    filename = f"comiccraft_{uuid.uuid4().hex[:8]}.pdf"
    file_path = EXPORT_DIR / filename
    pdf.output(str(file_path))

    return f"/static/exports/{filename}"
