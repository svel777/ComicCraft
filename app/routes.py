import asyncio
from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from .gemini_service import generate_comic_outline, generate_panel_image
from .pdf_exporter import save_pdf

router = APIRouter()
templates = Jinja2Templates(directory="templates")

BASE_DIR = Path(__file__).resolve().parent.parent

@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

@router.post("/generate")
async def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
    panels: int = Form(5),
):
    panel_count = max(3, min(int(panels), 6))

    data = type(
        "ComicInput",
        (),
        {
            "story_prompt": story_prompt,
            "character_name": character_name,
            "setting": setting,
            "tone": tone,
            "art_style": art_style,
            "panels": panel_count,
        },
    )()

    comic = await asyncio.to_thread(generate_comic_outline, data)

    sem = asyncio.Semaphore(2)

    async def process_panel(panel):
        async with sem:
            try:
                panel["image"] = await asyncio.wait_for(
                    asyncio.to_thread(
                        generate_panel_image,
                        panel["image_prompt"],
                        panel["number"],
                        comic["title"],
                    ),
                    timeout=120,
                )
            except Exception as exc:
                print(f"Panel {panel['number']} failed: {exc!r}")
                panel["image"] = ""

    await asyncio.gather(*(process_panel(p) for p in comic["panels"]))

    tasks = [asyncio.to_thread(process_panel, panel) for panel in comic["panels"]]
    await asyncio.gather(*tasks)

    # Generate PDF and write directly inside app/static/exports/
    try:
        comic["pdf"] = await asyncio.to_thread(save_pdf, comic)
    except Exception as exc:
        print(f"PDF generation error: {exc}")
        comic["pdf"] = ""

    return templates.TemplateResponse(
        request,
        "comic_preview.html",
        {
            "comic": comic,
        },
    )

@router.get("/download")
async def download_pdf(path: str):
    if not path:
        return JSONResponse({"error": "No PDF path provided"}, status_code=400)

    clean_path = path.lstrip("/")
    safe = APP_DIR / clean_path

    if not safe.exists():
        return JSONResponse(
            {"error": f"PDF file does not exist on server: {safe}"},
            status_code=404,
        )

    if safe.suffix.lower() != ".pdf":
        return JSONResponse(
            {"error": "Invalid file format"},
            status_code=400,
        )

    return FileResponse(
        path=safe,
        media_type="application/pdf",
        filename=safe.name,
        headers={"Content-Disposition": f'attachment; filename="{safe.name}"'}
    )

@router.get("/export-success")
async def export_success(request: Request):
    return templates.TemplateResponse(request, "export_success.html")

@router.get("/health")
async def health():
    return {"status": "ok", "service": "ComicCraft"}
