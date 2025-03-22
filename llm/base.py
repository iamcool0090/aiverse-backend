from abc import ABC, abstractmethod
import os 




class BaseLLM(ABC):
    def __init__(self):
        self._initialize_client()
        pass

    @abstractmethod
    def _initialize_client(self):
        pass

    @abstractmethod 
    def generate_speech(self, text):
        pass

    @abstractmethod
    def generate_character_speech(self, text, character_id):
        pass

