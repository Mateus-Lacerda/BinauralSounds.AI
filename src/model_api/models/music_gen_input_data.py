from pydantic import BaseModel


class MusicGenInputData(BaseModel):
    description: str
    binaural_freq: int
    apply_binaural: bool
