from pydantic import BaseModel
from typing import Dict

class SpeechRecognitionResult(BaseModel):
    """Model representing the result of a speech recognition operation."""
    text: str
    language: str

    def __str__(self) -> str:
        """String representation of the recognition result."""
        return f"Text: {self.text}, Language: {self.language}"
    
    def to_dict(self) -> Dict[str, str]:
        """Convert the result to a dictionary."""
        return {
            "text": self.text,
            "language": self.language
        }