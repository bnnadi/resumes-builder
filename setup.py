"""Setup configuration for ATS Resume Export System."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = [
        line.strip()
        for line in requirements_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="ats-resume-builder",
    version="0.4.0",
    description="AI-powered resume builder with ATS-optimized export",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Bisike Nnadi",
    author_email="",
    url="https://github.com/bisikennadi/resumes-builder",
    packages=find_packages(where="src", exclude=["tests", "tests.*"]),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={
        "resume_export": [
            "templates/*.yaml",
            "templates/*.docx",
        ],
        "resume_ai": [
            "prompts/*.txt",
        ],
    },
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "resume-builder=resume_builder_cli:main",
            "export-resume=resume_export.cli:main",
            "resume-export=resume_export.cli:main",
            "resume-skills=resume_ai.skills_cli:skills",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business",
        "Topic :: Text Processing :: Markup :: Markdown",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.12",
)

