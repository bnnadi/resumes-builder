"""
Ollama Client - Interface to local Ollama instance for AI processing.
"""

import requests
from typing import Optional
from dataclasses import dataclass
import sys


@dataclass
class OllamaConfig:
    """Configuration for Ollama client."""
    
    base_url: str = "http://localhost:11434"
    model: str = "llama3.1"
    temperature: float = 0.7
    timeout: int = 180  # 3 minutes for long responses
    
    
class OllamaClient:
    """Client for interacting with local Ollama instance."""
    
    def __init__(self, config: Optional[OllamaConfig] = None):
        """
        Initialize Ollama client.
        
        Args:
            config: Optional configuration. Uses defaults if not provided.
        """
        self.config = config or OllamaConfig()
        self._check_connection()
    
    def _check_connection(self) -> None:
        """
        Verify Ollama is running and accessible.
        
        Raises:
            RuntimeError: If cannot connect to Ollama
        """
        try:
            response = requests.get(
                f"{self.config.base_url}/api/tags",
                timeout=5
            )
            response.raise_for_status()
            
            # Check if our model is available
            data = response.json()
            models = [m["name"] for m in data.get("models", [])]
            
            if not any(self.config.model in m for m in models):
                print(f"⚠️  Warning: Model '{self.config.model}' not found.")
                print(f"Available models: {', '.join(models)}")
                print(f"\nTo install: ollama pull {self.config.model}")
                
        except requests.exceptions.ConnectionError:
            raise RuntimeError(
                "❌ Cannot connect to Ollama.\n\n"
                "Is Ollama running? Start it with:\n"
                "  ollama serve\n\n"
                "Or install Ollama:\n"
                "  brew install ollama  (macOS)\n"
                "  https://ollama.ai/download (other platforms)"
            )
        except Exception as e:
            raise RuntimeError(f"Error connecting to Ollama: {e}")
    
    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        stream: bool = False,
        verbose: bool = False
    ) -> str:
        """
        Generate response from Ollama.
        
        Args:
            prompt: User prompt
            system: System prompt (optional)
            stream: Stream response for real-time output
            verbose: Show generation progress
            
        Returns:
            Generated text response
            
        Raises:
            RuntimeError: If generation fails
        """
        if verbose:
            print(f"🤖 Generating with {self.config.model}...")
            if stream:
                print("📝 Response: ", end="", flush=True)
        
        payload = {
            "model": self.config.model,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "temperature": self.config.temperature
            }
        }
        
        if system:
            payload["system"] = system
        
        try:
            response = requests.post(
                f"{self.config.base_url}/api/generate",
                json=payload,
                timeout=self.config.timeout,
                stream=stream
            )
            response.raise_for_status()
            
            if stream:
                return self._handle_stream(response, verbose)
            else:
                result = response.json()["response"]
                if verbose:
                    print("✅ Done")
                return result
                
        except requests.exceptions.Timeout:
            raise RuntimeError(
                f"⏱️  Ollama request timed out after {self.config.timeout}s.\n"
                "Try using a smaller model or increasing timeout."
            )
        except Exception as e:
            raise RuntimeError(f"Ollama generation failed: {e}")
    
    def _handle_stream(self, response, verbose: bool) -> str:
        """
        Handle streaming response for real-time output.
        
        Args:
            response: Streaming response object
            verbose: Whether to print to console
            
        Returns:
            Complete response text
        """
        import json
        
        full_response = ""
        
        try:
            for line in response.iter_lines():
                if line:
                    data = json.loads(line.decode('utf-8'))
                    text = data.get("response", "")
                    
                    if verbose:
                        print(text, end="", flush=True)
                    
                    full_response += text
                    
                    # Check if done
                    if data.get("done", False):
                        break
            
            if verbose:
                print("\n✅ Done")
                
        except KeyboardInterrupt:
            if verbose:
                print("\n\n⚠️  Generation interrupted by user")
            raise
        
        return full_response
    
    def check_model(self, model_name: Optional[str] = None) -> bool:
        """
        Check if a specific model is available.
        
        Args:
            model_name: Model to check. Uses config model if not specified.
            
        Returns:
            True if model is available
        """
        model = model_name or self.config.model
        
        try:
            response = requests.get(f"{self.config.base_url}/api/tags")
            response.raise_for_status()
            
            data = response.json()
            models = [m["name"] for m in data.get("models", [])]
            
            return any(model in m for m in models)
            
        except Exception:
            return False

