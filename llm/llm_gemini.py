
from llm.base import BaseLLM
from database.db_sqlite import SQLiteDB
import os


from google import genai



class GeminiLLM(BaseLLM):
    def __init__(self):
        self._initialize_client()
        self.db = SQLiteDB()

    def _initialize_client(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def generate_speech(self, data):
        response = self.client.models.generate_content(
            model="gemini-2.0-pro-exp-02-05", contents=data
        )
        return response.text

    def generate_character_speech(self, data, character_id):
        character = self.db.get(character_id)
        additional_prompt = f"You are {character.name}. {character.prompt}"
        content = f"""{additional_prompt} You must answer the user questions in the same language as {data}.return raw text to speak. {data} """
        response = self.client.models.generate_content(
            model="gemini-2.0-pro-exp-02-05", contents=content, 
        )
        return response.text