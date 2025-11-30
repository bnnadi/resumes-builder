"""
Resume AI Module - Ollama-powered resume analysis and customization.

This module provides AI-powered features for:
- Job description analysis
- Resume matching and scoring
- Resume evaluation
- Resume customization
"""

__version__ = "0.1.0"

from .ollama_client import OllamaClient, OllamaConfig
from .job_match import JobMatcher, JobMatchResult
from .threshold_gate import ThresholdGate, ThresholdConfig, Decision

__all__ = [
    "OllamaClient",
    "OllamaConfig",
    "JobMatcher",
    "JobMatchResult",
    "ThresholdGate",
    "ThresholdConfig",
    "Decision",
]

