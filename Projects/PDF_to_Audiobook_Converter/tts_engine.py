"""
Text-to-Speech Conversion Engine
Handles conversion of text to speech using pyttsx3 and gTTS.
"""

import pyttsx3
from gtts import gTTS
import os
from typing import Optional
from pathlib import Path


class TTSEngine:
    """Convert text to speech with multiple options."""
    
    def __init__(self, engine_type: str = "pyttsx3"):
        """
        Initialize TTS engine.
        
        Args:
            engine_type: "pyttsx3" for offline or "gtts" for online
        """
        self.engine_type = engine_type
        self.engine = None
        self.current_speed = 150  # words per minute
        self.current_volume = 1.0  # 0.0 to 1.0
        
        if engine_type == "pyttsx3":
            self.engine = pyttsx3.init()
            self._setup_pyttsx3()
    
    def _setup_pyttsx3(self):
        """Configure pyttsx3 engine."""
        if self.engine:
            self.engine.setProperty('rate', self.current_speed)
            self.engine.setProperty('volume', self.current_volume)
            
            # List available voices
            voices = self.engine.getProperty('voices')
            if voices:
                self.engine.setProperty('voice', voices[0].id)
    
    def set_speed(self, speed: int):
        """
        Set speech speed (words per minute).
        
        Args:
            speed: Speed in WPM (typically 50-300)
        """
        self.current_speed = max(50, min(300, speed))
        if self.engine_type == "pyttsx3" and self.engine:
            self.engine.setProperty('rate', self.current_speed)
    
    def set_volume(self, volume: float):
        """
        Set volume level.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.current_volume = max(0.0, min(1.0, volume))
        if self.engine_type == "pyttsx3" and self.engine:
            self.engine.setProperty('volume', self.current_volume)
    
    def text_to_speech_pyttsx3(self, text: str, output_file: str) -> bool:
        """
        Convert text to speech using pyttsx3 and save as MP3.
        
        Args:
            text: Text to convert
            output_file: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.engine:
                self.engine = pyttsx3.init()
                self._setup_pyttsx3()
            
            # Save as WAV first (pyttsx3 limitation)
            wav_file = output_file.replace('.mp3', '.wav')
            self.engine.save_to_file(text, wav_file)
            self.engine.runAndWait()
            
            # Convert WAV to MP3 if needed
            if output_file.endswith('.mp3'):
                self._convert_wav_to_mp3(wav_file, output_file)
                if os.path.exists(wav_file):
                    os.remove(wav_file)
            
            return True
        except Exception as e:
            print(f"Error in pyttsx3 conversion: {e}")
            return False
    
    def text_to_speech_gtts(self, text: str, output_file: str, lang: str = 'en') -> bool:
        """
        Convert text to speech using gTTS and save as MP3.
        
        Args:
            text: Text to convert
            output_file: Output file path
            lang: Language code (default: 'en')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Split text into chunks (gTTS has character limit)
            chunks = self._split_text(text, 3000)
            
            if len(chunks) == 1:
                tts = gTTS(text=chunks[0], lang=lang, slow=False)
                tts.save(output_file)
            else:
                # Combine multiple chunks
                from pydub import AudioSegment
                combined = AudioSegment.empty()
                
                for i, chunk in enumerate(chunks):
                    temp_file = f"temp_chunk_{i}.mp3"
                    tts = gTTS(text=chunk, lang=lang, slow=False)
                    tts.save(temp_file)
                    combined += AudioSegment.from_mp3(temp_file)
                    os.remove(temp_file)
                
                combined.export(output_file, format="mp3")
            
            return True
        except Exception as e:
            print(f"Error in gTTS conversion: {e}")
            return False
    
    def convert_to_speech(self, text: str, output_file: str) -> bool:
        """
        Convert text to speech using configured engine.
        
        Args:
            text: Text to convert
            output_file: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        if self.engine_type == "pyttsx3":
            return self.text_to_speech_pyttsx3(text, output_file)
        else:
            return self.text_to_speech_gtts(text, output_file)
    
    @staticmethod
    def _split_text(text: str, max_length: int) -> list:
        """Split text into chunks for processing."""
        chunks = []
        current_chunk = ""
        
        for sentence in text.split('.'):
            if len(current_chunk) + len(sentence) < max_length:
                current_chunk += sentence + "."
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sentence + "."
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    @staticmethod
    def _convert_wav_to_mp3(wav_file: str, mp3_file: str):
        """Convert WAV to MP3 using pydub."""
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_wav(wav_file)
            audio.export(mp3_file, format="mp3")
        except Exception as e:
            print(f"Error converting WAV to MP3: {e}")
