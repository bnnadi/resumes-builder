"""
Allow running resume_export as a module: python -m resume_export
"""

import sys
from .cli import main

if __name__ == '__main__':
    sys.exit(main())

