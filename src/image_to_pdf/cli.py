"""
CLI entry point for Image to PDF Converter.
"""

import argparse
import sys
from pathlib import Path

from image_to_pdf.converter import ImageToPDFConverter


def main() -> int:
    """
    Main entry point for the CLI.

    Returns:
        Exit code (0 for success, 1 for failure).
    """
    parser = argparse.ArgumentParser(
        prog="image-to-pdf",
        description="Convert images to PDF with custom ordering and HEIC support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /path/to/images -o album.pdf
  %(prog)s photo1.jpg photo2.png -o combined.pdf
  %(prog)s  # Interactive mode
        """,
    )
    parser.add_argument(
        "inputs",
        nargs="*",
        help="Input images or directories (omit for interactive mode)",
    )
    parser.add_argument(
        "-o", "--output",
        help="Output PDF filename (default: converted_images.pdf)",
        default=None,
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="%(prog)s 1.0.0",
    )

    args = parser.parse_args()
    converter = ImageToPDFConverter()

    # Interactive mode if no inputs provided
    if not args.inputs:
        print("🖼️  Interactive Image to PDF Converter")
        print("=" * 40)

        input_path = input("Enter image file(s) or directory path: ").strip()
        if not input_path:
            print("❌ No input provided!")
            return 1

        # Parse input - treat as single path (don't split on spaces, paths can have spaces)
        input_paths = Path(input_path.strip('"').strip("'"))

        output_path = input(
            "Enter output PDF filename (press Enter for 'converted_images.pdf'): "
        ).strip()

        if not output_path:
            output_path = None  # Will be prompted later

        success = converter.run(input_paths, output_path)
    else:
        # CLI mode
        input_paths = [Path(p) for p in args.inputs]
        success = converter.run(
            input_paths if len(input_paths) > 1 else input_paths[0],
            args.output
        )

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
