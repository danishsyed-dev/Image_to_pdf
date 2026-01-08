"""
Package entry point for running as `python -m image_to_pdf`.
"""

import sys

from image_to_pdf.cli import main

if __name__ == "__main__":
    sys.exit(main())
