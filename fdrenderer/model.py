from typing import Optional

from pydantic import BaseModel


class DropFile(BaseModel):
    AudiofilePath: str
    Subtitles: Optional[str]
    Delay: float