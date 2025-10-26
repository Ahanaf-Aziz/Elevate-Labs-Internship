"""
PDF Text Extraction Module
Handles loading and extracting text from PDF files with cleaning and validation.
"""

import fitz  # PyMuPDF
import re
from typing import List, Tuple


class PDFExtractor:
    """Extract and clean text from PDF files."""
    
    def __init__(self, pdf_path: str):
        """Initialize with PDF file path."""
        self.pdf_path = pdf_path
        self.document = None
        self.text_content = ""
        
    def load_pdf(self) -> bool:
        """Load PDF document."""
        try:
            self.document = fitz.open(self.pdf_path)
            return True
        except Exception as e:
            print(f"Error loading PDF: {e}")
            return False
    
    def extract_text(self) -> str:
        """Extract text from all pages."""
        if not self.document:
            return ""
        
        extracted_text = []
        for page_num in range(len(self.document)):
            page = self.document[page_num]
            text = page.get_text()
            
            # Skip empty pages
            if text.strip():
                extracted_text.append(text)
        
        self.text_content = "\n".join(extracted_text)
        return self.text_content
    
    def clean_text(self) -> str:
        """Clean and normalize extracted text."""
        if not self.text_content:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', self.text_content)
        
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\-\:\;\'\"]', '', text)
        
        # Fix spacing around punctuation
        text = re.sub(r'\s+([.,!?;:])', r'\1', text)
        
        # Remove multiple spaces
        text = re.sub(r' +', ' ', text)
        
        return text.strip()
    
    def get_page_count(self) -> int:
        """Get total number of pages."""
        return len(self.document) if self.document else 0
    
    def extract_by_pages(self) -> List[str]:
        """Extract text page by page."""
        if not self.document:
            return []
        
        pages_text = []
        for page_num in range(len(self.document)):
            page = self.document[page_num]
            text = page.get_text().strip()
            if text:  # Only include non-empty pages
                pages_text.append(text)
        
        return pages_text
    
    def close(self):
        """Close the PDF document."""
        if self.document:
            self.document.close()
