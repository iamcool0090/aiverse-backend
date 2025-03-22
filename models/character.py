from pydantic import BaseModel
from typing import Optional

class CharactersModel(BaseModel):
    id: Optional[int] = None  # ID is optional because it's auto-generated
    name: str
    prompt: str
    profile_image_url: str

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "prompt": self.prompt,
            "profile_image_url": self.profile_image_url if self.profile_image_url else ""
        }

    class Config:
        orm_mode = True