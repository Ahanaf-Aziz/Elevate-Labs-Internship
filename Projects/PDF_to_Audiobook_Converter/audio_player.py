"""
Audio Playback and Control Module
Handles playing and exporting audio files.
"""

import pygame
import os
from typing import Optional


class AudioPlayer:
    """Handle audio playback with controls."""
    
    def __init__(self):
        """Initialize audio player."""
        pygame.mixer.init()
        self.is_playing = False
        self.is_paused = False
        self.current_file = None
    
    def play(self, audio_file: str) -> bool:
        """
        Play audio file.
        
        Args:
            audio_file: Path to audio file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not os.path.exists(audio_file):
                print(f"Audio file not found: {audio_file}")
                return False
            
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            self.is_playing = True
            self.is_paused = False
            self.current_file = audio_file
            return True
        except Exception as e:
            print(f"Error playing audio: {e}")
            return False
    
    def pause(self) -> bool:
        """Pause playback."""
        try:
            if self.is_playing and not self.is_paused:
                pygame.mixer.music.pause()
                self.is_paused = True
                return True
            return False
        except Exception as e:
            print(f"Error pausing audio: {e}")
            return False
    
    def resume(self) -> bool:
        """Resume playback."""
        try:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
                return True
            return False
        except Exception as e:
            print(f"Error resuming audio: {e}")
            return False
    
    def stop(self) -> bool:
        """Stop playback."""
        try:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.is_paused = False
            return True
        except Exception as e:
            print(f"Error stopping audio: {e}")
            return False
    
    def set_volume(self, volume: float):
        """
        Set playback volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(volume)
    
    def get_busy(self) -> bool:
        """Check if audio is currently playing."""
        return pygame.mixer.music.get_busy()
    
    def get_position(self) -> float:
        """Get current playback position in seconds."""
        if self.is_playing:
            return pygame.mixer.music.get_pos() / 1000.0
        return 0.0
