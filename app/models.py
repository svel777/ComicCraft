from pydantic import BaseModel, Field

class ComicRequest(BaseModel):
    story_prompt: str = Field(min_length=3, max_length=1000)
    character_name: str = Field(min_length=1, max_length=80)
    setting: str = Field(default="enchanted forest", max_length=120)
    tone: str = Field(default="funny", max_length=50)
    art_style: str = Field(default="cute cartoon", max_length=80)
    panels: int = Field(default=5, ge=3, le=6)

class Panel(BaseModel):
    number: int
    title: str
    scene: str
    narration: str
    dialogue: str
    caption: str
    image_prompt: str

class Comic(BaseModel):
    title: str
    tagline: str
    panels: list[Panel]
