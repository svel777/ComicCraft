# ComicCraft — AI Comic Story Creator

A creative FastAPI + Jinja2 web app that turns a user's story idea into a multi-panel comic using Google's Gemini API.

## 1. Open in VS Code

Open the `ComicCraft` folder in VS Code.

## 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Windows CMD:

```bat
python -m venv .venv
.venv\Scripts\activate
```

macOS / Linux Terminal (bash/zsh):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install packages

```bash
pip install -r requirements.txt
```

## 4. Add your Google AI API key

Copy `.env.example` to `.env` by:
```bash
cp .env.example .env # Linux
# (or)
copy .env.example .env # Windows
```
and put your key in
```env
GEMINI_API_KEY=YOUR_KEY_HERE
```

## 5. Run

```bash
uvicorn app.main:app --reload --port 8000
```

Open:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs


## API example

POST `/generate-comic/json`

```json
{
  "story_prompt": "A brave fox exploring an enchanted forest",
  "character_name": "Finn",
  "setting": "Enchanted forest",
  "tone": "Adventurous",
  "art_style": "Cute cartoon",
  "panels": 5
}
```
