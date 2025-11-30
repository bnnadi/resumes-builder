"""
ATS Resume Export System

A tool for converting markdown resumes to ATS-optimized .docx files
with automatic validation and package building.
"""

__version__ = "0.1.0"
__author__ = "Bisike Nnadi"

from .parser import ResumeParser
from .docx_builder import DocxBuilder
from .exporter import ResumeExporter

__all__ = ["ResumeParser", "DocxBuilder", "ResumeExporter", "__version__"]

