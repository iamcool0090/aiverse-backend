from pydantic import BaseModel
from fastapi import UploadFile, File


class ConversationRequest(BaseModel):
    audio: UploadFile

    class Config:
        arbitrary_types_allowed = True


class ConversationResponse(BaseModel):
    audio: bytes


class CharacterAddRequest(BaseModel):
    id: int
    name : str
    prompt : str
    profile_image_url : str

