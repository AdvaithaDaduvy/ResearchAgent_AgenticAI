from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class ResearchReaderInput(BaseModel):
    file_path: str = Field(..., description="Absolute path to the PDF file")

class ResearchPaperReaderTool(BaseTool):
    name: str = "Research Paper Reader"
    description: str = "Reads and extracts raw text from a research paper PDF"
    args_schema: Type[BaseModel] = ResearchReaderInput

    def _run(self, file_path: str) -> str:
        from PyPDF2 import PdfReader
        try:
            reader = PdfReader(file_path)
            text = "".join(page.extract_text() or "" for page in reader.pages)
            return text
        except Exception as e:
            return f"Error reading PDF: {e}"
