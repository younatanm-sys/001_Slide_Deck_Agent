"""
Document Parser for LLAPI
=========================

Parses source documents (text, markdown, PDF) into content that can be
processed by the LLM content generator.
"""

from pathlib import Path
from typing import Optional
import re


class DocumentParser:
    """Parse various document formats into text content for LLM processing."""

    SUPPORTED_FORMATS = ['.txt', '.md', '.markdown', '.pdf']

    def __init__(self):
        """Initialize the document parser."""
        pass

    def parse(self, source: str) -> str:
        """
        Parse a document or raw text into content string.

        Args:
            source: Either a file path or raw text content

        Returns:
            Parsed text content
        """
        # Check if source is a file path
        if self._is_file_path(source):
            return self.parse_file(source)
        else:
            # Assume it's raw text
            return self._clean_text(source)

    def parse_file(self, file_path: str) -> str:
        """
        Parse a file into text content.

        Args:
            file_path: Path to the source file

        Returns:
            Parsed text content

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is not supported
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        suffix = path.suffix.lower()

        if suffix not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported file format: {suffix}. "
                f"Supported formats: {', '.join(self.SUPPORTED_FORMATS)}"
            )

        if suffix in ['.txt', '.md', '.markdown']:
            return self._parse_text_file(path)
        elif suffix == '.pdf':
            return self._parse_pdf_file(path)

    def _is_file_path(self, source: str) -> bool:
        """Check if source looks like a file path."""
        # If it contains newlines, it's probably raw text
        if '\n' in source and len(source) > 500:
            return False

        # Check if it looks like a path
        path = Path(source)
        return path.suffix.lower() in self.SUPPORTED_FORMATS or path.exists()

    def _parse_text_file(self, path: Path) -> str:
        """Parse a text or markdown file."""
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        return self._clean_text(content)

    def _parse_pdf_file(self, path: Path) -> str:
        """
        Parse a PDF file.

        Note: Requires PyPDF2 or pdfplumber to be installed.
        Falls back to error message if not available.
        """
        try:
            import PyPDF2

            with open(path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text_parts = []
                for page in reader.pages:
                    text_parts.append(page.extract_text())
                return self._clean_text('\n'.join(text_parts))

        except ImportError:
            try:
                import pdfplumber

                with pdfplumber.open(path) as pdf:
                    text_parts = []
                    for page in pdf.pages:
                        text_parts.append(page.extract_text() or '')
                    return self._clean_text('\n'.join(text_parts))

            except ImportError:
                raise ImportError(
                    "PDF parsing requires PyPDF2 or pdfplumber. "
                    "Install with: pip install PyPDF2 or pip install pdfplumber"
                )

    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize text content.

        Args:
            text: Raw text content

        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r' {2,}', ' ', text)

        # Remove common markdown artifacts if needed
        # (but keep structure for context)

        # Strip leading/trailing whitespace
        text = text.strip()

        return text

    def extract_sections(self, content: str) -> dict:
        """
        Extract sections from structured content (markdown headers, etc.)

        Args:
            content: Parsed text content

        Returns:
            Dictionary with section names as keys and content as values
        """
        sections = {}
        current_section = "introduction"
        current_content = []

        for line in content.split('\n'):
            # Check for markdown headers
            if line.startswith('#'):
                # Save previous section
                if current_content:
                    sections[current_section] = '\n'.join(current_content).strip()

                # Start new section
                current_section = line.lstrip('#').strip().lower()
                current_section = re.sub(r'[^a-z0-9_]', '_', current_section)
                current_content = []
            else:
                current_content.append(line)

        # Save last section
        if current_content:
            sections[current_section] = '\n'.join(current_content).strip()

        return sections

    def get_word_count(self, content: str) -> int:
        """Get word count of content."""
        return len(content.split())

    def get_estimated_slides(self, content: str, words_per_slide: int = 100) -> int:
        """
        Estimate number of slides based on content length.

        Args:
            content: Text content
            words_per_slide: Average words per slide (default: 100)

        Returns:
            Estimated number of slides
        """
        word_count = self.get_word_count(content)
        return max(5, min(20, word_count // words_per_slide))
