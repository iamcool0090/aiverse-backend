"""
Azure Speech Service Client
--------------------------
A clean implementation for Azure Speech Cognitive Services with speech recognition 
and synthesis capabilities supporting multiple languages.
"""

import os
from typing import Dict, List, Optional
import azure.cognitiveservices.speech as speechsdk
from pydantic import BaseModel
from models.speech import SpeechRecognitionResult 



class AzureSpeechClient:
    """Client for Azure Speech Services supporting recognition and synthesis."""
    
    def __init__(
        self, 
        speech_key: Optional[str] = None, 
        speech_region: Optional[str] = None,
        supported_languages: Optional[List[str]] = None
    ):
        """
        Initialize the Azure Speech Client.
        
        Args:
            speech_key: Azure Speech API key (defaults to AZURE_SPEECH_KEY env var)
            speech_region: Azure region (defaults to AZURE_SPEECH_REGION env var)
            supported_languages: List of languages to support for auto-detection
        """
        self.speech_key = speech_key or os.getenv("AZURE_SPEECH_KEY")
        self.speech_region = speech_region or os.getenv("AZURE_SPEECH_REGION")
        
        if not self.speech_key or not self.speech_region:
            raise ValueError("Azure Speech credentials not found. Set AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables.")
        
        self.supported_languages = supported_languages or ["en-US", "hi-IN", "kn-IN"]
        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_key, 
            region=self.speech_region
        )
        
        # Voice mapping for different languages
        self.voice_map = {
            # Indian languages
            "en-US": "en-US-JennyMultilingualNeural",
            "hi-IN": "hi-IN-SwaraNeural",
            "kn-IN": "kn-IN-SapnaNeural",
            "ta-IN": "ta-IN-PallaviNeural",
            "te-IN": "te-IN-ShrutiNeural",
            "mr-IN": "mr-IN-AarohiNeural",
            "bn-IN": "bn-IN-BashkarNeural",
            "gu-IN": "gu-IN-DhwaniNeural", 
            "ml-IN": "ml-IN-SobhanaNeural",
            "pa-IN": "pa-IN-GurleenNeural",
            
            # International languages
            "es-ES": "es-ES-ElviraNeural",
            "fr-FR": "fr-FR-DeniseNeural",
            "de-DE": "de-DE-KatjaNeural",
            "it-IT": "it-IT-ElsaNeural",
            "ja-JP": "ja-JP-NanamiNeural",
            "zh-CN": "zh-CN-XiaoxiaoNeural",
            "ru-RU": "ru-RU-SvetlanaNeural",
            "pt-BR": "pt-BR-FranciscaNeural",
            "ar-SA": "ar-SA-ZariyahNeural"
        }

    async def recognize_from_file(self, file_path: str) -> SpeechRecognitionResult:
        """
        Recognize speech from an audio file with automatic language detection.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            SpeechRecognitionResult with recognized text and detected language
        """
        auto_detect_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
            languages=self.supported_languages
        )
        audio_config = speechsdk.AudioConfig(filename=file_path)
        
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config, 
            audio_config=audio_config, 
            auto_detect_source_language_config=auto_detect_config
        )
        
        result = speech_recognizer.recognize_once_async().get()
        detected_language = speechsdk.AutoDetectSourceLanguageResult(result).language
        
        return SpeechRecognitionResult(
            text=result.text, 
            language=detected_language
        )

    async def synthesize_speech(
        self, 
        text: str, 
        language: str, 
        output_file: str = "output.wav"
    ) -> bool:
        """
        Synthesize speech from text in the specified language.
        
        Args:
            text: Text to convert to speech
            language: Language code (e.g., "en-US")
            output_file: Path to save the audio file
            
        Returns:
            True if synthesis was successful, False otherwise
        """
        # Update speech config with appropriate voice
        self.speech_config.speech_synthesis_voice_name = self.get_voice_for_language(language)
        
        # Create speech synthesizer
        speech_synthesizer = speechsdk.SpeechSynthesizer(self.speech_config, None)

        # Synthesize speech
        result = speech_synthesizer.speak_text_async(text).get()
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            with open(output_file, "wb+") as file:
                file.write(result.audio_data)
            return True
            
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation = result.cancellation_details
            print(f"Speech synthesis canceled: {cancellation.reason}")
            if cancellation.reason == speechsdk.CancellationReason.Error:
                print(f"Error details: {cancellation.error_details}")
            return False

    def get_voice_for_language(self, language: str) -> str:
        """
        Get the appropriate voice for the specified language.
        
        Args:
            language: Language code (e.g., "en-US")
            
        Returns:
            Voice name for the specified language
        """
        return self.voice_map.get(language, "en-US-JennyMultilingualNeural")


# Usage example
if __name__ == "__main__":
    import asyncio
    import dotenv
    
    # Load environment variables
    dotenv.load_dotenv()
    
    async def main():
        # Initialize client
        speech_client = AzureSpeechClient()
        
        # Example: Speech recognition
        result = await speech_client.recognize_from_file("sample.wav")
        print(f"Recognized: {result}")
        
        # Example: Speech synthesis
        success = await speech_client.synthesize_speech(
            "Hello, this is a test of the Azure Speech Service.", 
            "en-US",
            "greeting.wav"
        )
        print(f"Synthesis successful: {success}")
    
    # Run the async example
    asyncio.run(main())