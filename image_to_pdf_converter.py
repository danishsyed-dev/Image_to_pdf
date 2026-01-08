#!/usr/bin/env python3
"""
Image to PDF Converter - Backward Compatibility Wrapper

This file is kept for backward compatibility. For new usage, please use:
    - CLI: image-to-pdf [options]
    - Module: python -m image_to_pdf [options]
    - Import: from image_to_pdf import ImageToPDFConverter

See README.md for full documentation.
"""

import sys
import warnings

# Show deprecation warning for direct script usage
warnings.warn(
    "Direct usage of image_to_pdf_converter.py is deprecated. "
    "Please use 'image-to-pdf' or 'python -m image_to_pdf' instead.",
    DeprecationWarning,
    stacklevel=2
)

# Import from the new package location
try:
    from src.image_to_pdf.converter import ImageToPDFConverter
    from src.image_to_pdf.cli import main
except ImportError:
    # Fallback for when package is installed
    from image_to_pdf.converter import ImageToPDFConverter
    from image_to_pdf.cli import main

# Re-export for backward compatibility
__all__ = ["ImageToPDFConverter", "main"]

if __name__ == "__main__":
    sys.exit(main())