"""
PDF to Audiobook Converter GUI Application
Main Tkinter interface for the converter.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from pathlib import Path
from pdf_extractor import PDFExtractor
from tts_engine import TTSEngine
from audio_player import AudioPlayer
import threading


class PDFAudiobookConverterGUI:
    """Main GUI application for PDF to Audiobook conversion."""
    
    def __init__(self, root):
        """Initialize the GUI application."""
        self.root = root
        self.root.title("PDF to Audiobook Converter")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Initialize components
        self.pdf_extractor = None
        self.tts_engine = TTSEngine(engine_type="pyttsx3")
        self.audio_player = AudioPlayer()
        self.current_text = ""
        self.conversion_thread = None
        
        # Create GUI
        self._create_widgets()
        self._setup_styles()
    
    def _setup_styles(self):
        """Setup custom styles for the GUI."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'))
        style.configure('Header.TLabel', font=('Helvetica', 12, 'bold'))
        style.configure('Normal.TLabel', font=('Helvetica', 10))
    
    def _create_widgets(self):
        """Create GUI widgets."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="PDF to Audiobook Converter", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # File Selection Section
        file_frame = ttk.LabelFrame(main_frame, text="Step 1: Select PDF File", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.file_label = ttk.Label(file_frame, text="No file selected", style='Normal.TLabel')
        self.file_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        browse_btn = ttk.Button(file_frame, text="Browse PDF", command=self._browse_pdf)
        browse_btn.grid(row=0, column=1, padx=5)
        
        # Text Preview Section
        preview_frame = ttk.LabelFrame(main_frame, text="Step 2: Text Preview", padding="10")
        preview_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Text widget with scrollbar
        scrollbar = ttk.Scrollbar(preview_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.text_widget = tk.Text(preview_frame, height=8, width=80, yscrollcommand=scrollbar.set)
        self.text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.config(command=self.text_widget.yview)
        
        # Conversion Settings Section
        settings_frame = ttk.LabelFrame(main_frame, text="Step 3: Conversion Settings", padding="10")
        settings_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Speed control
        ttk.Label(settings_frame, text="Speech Speed (WPM):", style='Normal.TLabel').grid(row=0, column=0, sticky=tk.W)
        self.speed_var = tk.IntVar(value=150)
        speed_scale = ttk.Scale(settings_frame, from_=50, to=300, orient=tk.HORIZONTAL, 
                               variable=self.speed_var, command=self._update_speed)
        speed_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        self.speed_label = ttk.Label(settings_frame, text="150 WPM", style='Normal.TLabel')
        self.speed_label.grid(row=0, column=2)
        
        # Volume control
        ttk.Label(settings_frame, text="Volume:", style='Normal.TLabel').grid(row=1, column=0, sticky=tk.W, pady=5)
        self.volume_var = tk.DoubleVar(value=1.0)
        volume_scale = ttk.Scale(settings_frame, from_=0.0, to=1.0, orient=tk.HORIZONTAL,
                                variable=self.volume_var, command=self._update_volume)
        volume_scale.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        self.volume_label = ttk.Label(settings_frame, text="100%", style='Normal.TLabel')
        self.volume_label.grid(row=1, column=2)
        
        # Engine selection
        ttk.Label(settings_frame, text="TTS Engine:", style='Normal.TLabel').grid(row=2, column=0, sticky=tk.W, pady=5)
        self.engine_var = tk.StringVar(value="pyttsx3")
        engine_combo = ttk.Combobox(settings_frame, textvariable=self.engine_var, 
                                   values=["pyttsx3", "gTTS"], state="readonly", width=15)
        engine_combo.grid(row=2, column=1, sticky=tk.W, padx=5)
        
        # Conversion Section
        conversion_frame = ttk.LabelFrame(main_frame, text="Step 4: Convert & Play", padding="10")
        conversion_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        convert_btn = ttk.Button(conversion_frame, text="Convert to Audio", command=self._convert_to_audio)
        convert_btn.grid(row=0, column=0, padx=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(conversion_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        self.status_label = ttk.Label(conversion_frame, text="Ready", style='Normal.TLabel')
        self.status_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Playback Controls Section
        playback_frame = ttk.LabelFrame(main_frame, text="Step 5: Playback Controls", padding="10")
        playback_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        play_btn = ttk.Button(playback_frame, text="Play", command=self._play_audio)
        play_btn.grid(row=0, column=0, padx=5)
        
        pause_btn = ttk.Button(playback_frame, text="Pause", command=self._pause_audio)
        pause_btn.grid(row=0, column=1, padx=5)
        
        resume_btn = ttk.Button(playback_frame, text="Resume", command=self._resume_audio)
        resume_btn.grid(row=0, column=2, padx=5)
        
        stop_btn = ttk.Button(playback_frame, text="Stop", command=self._stop_audio)
        stop_btn.grid(row=0, column=3, padx=5)
        
        export_btn = ttk.Button(playback_frame, text="Export as MP3", command=self._export_audio)
        export_btn.grid(row=0, column=4, padx=5)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        conversion_frame.columnconfigure(1, weight=1)
        settings_frame.columnconfigure(1, weight=1)
    
    def _browse_pdf(self):
        """Browse and select a PDF file."""
        file_path = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if file_path:
            self.pdf_extractor = PDFExtractor(file_path)
            if self.pdf_extractor.load_pdf():
                self.file_label.config(text=f"File: {os.path.basename(file_path)}")
                self._extract_and_preview()
            else:
                messagebox.showerror("Error", "Failed to load PDF file")
    
    def _extract_and_preview(self):
        """Extract text from PDF and show preview."""
        if not self.pdf_extractor:
            return
        
        self.status_label.config(text="Extracting text...")
        self.root.update()
        
        text = self.pdf_extractor.extract_text()
        cleaned_text = self.pdf_extractor.clean_text()
        self.current_text = cleaned_text
        
        # Show preview
        preview_text = cleaned_text[:500] + "..." if len(cleaned_text) > 500 else cleaned_text
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(1.0, preview_text)
        
        page_count = self.pdf_extractor.get_page_count()
        self.status_label.config(text=f"Extracted {page_count} pages. Ready to convert.")
    
    def _update_speed(self, value):
        """Update speech speed."""
        speed = int(float(value))
        self.tts_engine.set_speed(speed)
        self.speed_label.config(text=f"{speed} WPM")
    
    def _update_volume(self, value):
        """Update volume."""
        volume = float(value)
        self.tts_engine.set_volume(volume)
        self.audio_player.set_volume(volume)
        percentage = int(volume * 100)
        self.volume_label.config(text=f"{percentage}%")
    
    def _convert_to_audio(self):
        """Convert PDF text to audio."""
        if not self.current_text:
            messagebox.showwarning("Warning", "Please select and extract a PDF first")
            return
        
        # Ask for output file
        output_file = filedialog.asksaveasfilename(
            defaultextension=".mp3",
            filetypes=[("MP3 files", "*.mp3"), ("All files", "*.*")]
        )
        
        if not output_file:
            return
        
        # Run conversion in separate thread
        self.conversion_thread = threading.Thread(
            target=self._conversion_worker,
            args=(output_file,)
        )
        self.conversion_thread.start()
    
    def _conversion_worker(self, output_file):
        """Worker thread for audio conversion."""
        try:
            self.status_label.config(text="Converting to audio... This may take a while")
            self.progress_var.set(0)
            self.root.update()
            
            engine = self.engine_var.get()
            self.tts_engine.engine_type = engine
            
            success = self.tts_engine.convert_to_speech(self.current_text, output_file)
            
            if success:
                self.status_label.config(text=f"Conversion complete! Saved to {os.path.basename(output_file)}")
                self.progress_var.set(100)
                messagebox.showinfo("Success", f"Audio file saved successfully!\n{output_file}")
            else:
                self.status_label.config(text="Conversion failed")
                messagebox.showerror("Error", "Failed to convert text to audio")
        except Exception as e:
            self.status_label.config(text="Conversion error")
            messagebox.showerror("Error", f"Conversion error: {str(e)}")
    
    def _play_audio(self):
        """Play the converted audio."""
        audio_file = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[("MP3 files", "*.mp3"), ("WAV files", "*.wav"), ("All files", "*.*")]
        )
        
        if audio_file:
            if self.audio_player.play(audio_file):
                self.status_label.config(text=f"Playing: {os.path.basename(audio_file)}")
            else:
                messagebox.showerror("Error", "Failed to play audio file")
    
    def _pause_audio(self):
        """Pause audio playback."""
        if self.audio_player.pause():
            self.status_label.config(text="Audio paused")
        else:
            messagebox.showwarning("Warning", "No audio is currently playing")
    
    def _resume_audio(self):
        """Resume audio playback."""
        if self.audio_player.resume():
            self.status_label.config(text="Audio resumed")
        else:
            messagebox.showwarning("Warning", "No paused audio to resume")
    
    def _stop_audio(self):
        """Stop audio playback."""
        if self.audio_player.stop():
            self.status_label.config(text="Audio stopped")
        else:
            messagebox.showwarning("Warning", "No audio is currently playing")
    
    def _export_audio(self):
        """Export audio to MP3."""
        messagebox.showinfo("Info", "Use 'Convert to Audio' to save as MP3")


def main():
    """Run the application."""
    root = tk.Tk()
    app = PDFAudiobookConverterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
