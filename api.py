from fastapi import FastAPI, UploadFile, File
from models.api import ConversationRequest, CharacterAddRequest
from fastapi.responses import FileResponse
from speech import AzureSpeechClient
from llm.llm_gemini import GeminiLLM

from fastapi.middleware.cors import CORSMiddleware

from database.db_sqlite import SQLiteDB

import dotenv
dotenv.load_dotenv()

# Initialize FastAPI application
app = FastAPI(
    title="Character Speech API",
    description="API for processing audio and generating character speech responses",
    version="1.0.0"
)

# Initialize service clients
speech_client = AzureSpeechClient()
llm_client = GeminiLLM()  # Using Gemini as the default LLM
database = SQLiteDB()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins - restrict this in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.post("/v1/upload", summary="Process audio and generate response")
async def upload_audio(audio: UploadFile = File(...)):
    """
    Process an uploaded audio file and generate a response using LLM.
    
    Args:
        audio (UploadFile): The audio file to process
        
    Returns:
        FileResponse: The generated audio response file
        
    Raises:
        Exception: If audio processing or speech synthesis fails
    """
    try:
        # Save uploaded file to a temporary location
        temp_file_path = f"/tmp/{audio.filename}"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(await audio.read())

        # Process the audio file with speech-to-text
        audio_transcription = None
        try:
            audio_transcription = await speech_client.recognize_from_file(temp_file_path)
        except Exception as e:
            return {"error": f"Speech-to-text processing failed: {str(e)}"}
        
        # Generate response text using LLM
        try:
            response_text = llm_client.generate_speech(audio_transcription.text)
        except Exception as e:
            return {"error": f"LLM response generation failed: {str(e)}"}

        # Synthesize speech from the generated text
        output_file_path = "output.wav"
        await speech_client.synthesize_speech(response_text, audio_transcription.language)

        return FileResponse(output_file_path, media_type="audio/wav")
    except Exception as e:
        return {"error": f"General processing error: {str(e)}"}
    finally:
        # Cleanup would go here if needed
        pass


@app.post('/v1/character/{character_id}/upload', summary="Process audio for a specific character")
async def upload_character_conversation(character_id: int, audio: UploadFile = File(...)):
    """
    Process an audio file and generate a character-specific response.
    
    Args:
        character_id (int): The ID of the character to generate a response for
        audio (UploadFile): The audio file containing the user's speech
        
    Returns:
        FileResponse: The generated audio response from the character
        
    Raises:
        Exception: If audio processing or speech synthesis fails
    """
    try:
        # Save uploaded file to a temporary location
        temp_file_path = f"/home/razor/{audio.filename}"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(await audio.read())

        # Process the audio file with speech-to-text
        audio_transcription = None
        try:
            audio_transcription = await speech_client.recognize_from_file(temp_file_path)
        except Exception as e:
            return {"error": f"Speech-to-text processing failed: {str(e)}"}
        
        # Generate character-specific response using LLM
        try:
            character_response = llm_client.generate_character_speech(
                audio_transcription.text, 
                character_id
            )
            
            # Synthesize speech from the generated text
            output_file_path = "output.wav"
            await speech_client.synthesize_speech(
                character_response, 
                audio_transcription.language
            )
            
            return FileResponse(output_file_path, media_type="audio/wav")
        except Exception as e:
            return {"error": f"Character response generation failed: {str(e)}"}

    except Exception as e:
        return {"error": f"General processing error: {str(e)}"}
    finally:
        # Cleanup would go here if needed
        pass


@app.get('/v1/characters/{character_id}', summary="Get character details")
async def get_character(character_id: int):
    """
    Retrieve a character by ID.
    
    Args:
        character_id (int): The ID of the character to retrieve
        
    Returns:
        dict: Character information
    """
    character = database.get(character_id)
    return character.to_dict()


@app.get('/v1/characters', summary="Get all characters")
async def get_characters():
    """
    Retrieve all available characters.
    
    Returns:
        list: List of all characters
    """
    characters = database.get_all_characters()
    return [character.to_dict() for character in characters]


@app.post('/v1/characters', summary="Add a new character")
async def add_character(request: CharacterAddRequest):
    """
    Add a new character to the database.
    
    Args:
        request (CharacterAddRequest): Character details
        
    Returns:
        dict: The ID of the newly created character
    """
    character_id = database.add(request)
    return {"id": character_id}