"""
Image to PDF Converter - Core Module

This module provides the ImageToPDFConverter class for converting images to PDF.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import List, Optional, Set, Union

import pillow_heif
from PIL import Image

# Register HEIF opener with Pillow
pillow_heif.register_heif_opener()


class ImageToPDFConverter:
    """
    A converter class that transforms images into PDF documents.

    Supports multiple image formats including JPG, PNG, WEBP, HEIC/HEIF, BMP, and TIFF.
    Provides both programmatic API and interactive CLI features.

    Attributes:
        supported_formats: Set of supported image file extensions.

    Example:
        >>> converter = ImageToPDFConverter()
        >>> images = converter.find_images("/path/to/images")
        >>> converter.convert_to_pdf(images, "output.pdf")
    """

    def __init__(self) -> None:
        """Initialize the converter with supported image formats."""
        self.supported_formats: Set[str] = {
            ".jpg", ".jpeg", ".png", ".webp",
            ".heic", ".heif", ".bmp", ".tiff", ".tif"
        }

    def find_images(
        self,
        directory_or_files: Union[str, Path, List[Union[str, Path]]]
    ) -> List[str]:
        """
        Find all supported images in the given directory or file list.

        Args:
            directory_or_files: A single path (file or directory) or a list of paths
                to search for images.

        Returns:
            A sorted list of absolute paths to found images.

        Example:
            >>> converter = ImageToPDFConverter()
            >>> images = converter.find_images("/path/to/photos")
            >>> print(f"Found {len(images)} images")
        """
        images: List[str] = []

        if isinstance(directory_or_files, (str, Path)):
            path = Path(directory_or_files)
            if path.is_dir():
                for file in path.iterdir():
                    if file.is_file() and file.suffix.lower() in self.supported_formats:
                        images.append(str(file.resolve()))
            elif path.is_file():
                if path.suffix.lower() in self.supported_formats:
                    images.append(str(path.resolve()))
        else:
            for item in directory_or_files:
                item_path = Path(item)
                if item_path.is_file():
                    if item_path.suffix.lower() in self.supported_formats:
                        images.append(str(item_path.resolve()))
                elif item_path.is_dir():
                    for file in item_path.iterdir():
                        if file.is_file() and file.suffix.lower() in self.supported_formats:
                            images.append(str(file.resolve()))

        return sorted(images)

    def display_images_with_numbers(self, images: List[str]) -> None:
        """
        Display a numbered list of images to the console.

        Args:
            images: List of image file paths to display.
        """
        print("\n" + "=" * 60)
        print("FOUND IMAGES:")
        print("=" * 60)
        for i, img_path in enumerate(images, 1):
            filename = os.path.basename(img_path)
            print(f"{i:2d}. {filename}")
        print("=" * 60)

    def get_user_ordering_preference(self, images: List[str]) -> List[str]:
        """
        Interactively get the user's preferred image order.

        Args:
            images: List of image file paths to order.

        Returns:
            List of image paths in the user's preferred order.
        """
        self.display_images_with_numbers(images)
        print("\nHow would you like to arrange these images in the PDF?")
        print("1. Default order (as listed above)")
        print("2. Custom order (specify by numbers)")

        while True:
            choice = input("\nEnter your choice (1 or 2): ").strip()
            if choice == "1":
                return images
            elif choice == "2":
                return self._get_custom_order(images)
            else:
                print("Invalid choice. Please enter 1 or 2.")

    def _get_custom_order(self, images: List[str]) -> List[str]:
        """
        Get custom ordering from user input.

        Args:
            images: List of image file paths to reorder.

        Returns:
            List of image paths in the custom order.
        """
        print(f"\nEnter the order using numbers 1-{len(images)} separated by spaces.")
        print("Example: 3 1 4 2 5 (to put image 3 first, then 1, then 4, etc.)")

        while True:
            try:
                order_input = input("Order: ").strip()
                order_numbers = [int(x.strip()) for x in order_input.split()]

                if len(order_numbers) != len(images):
                    print(f"Error: Please specify exactly {len(images)} numbers.")
                    continue

                if set(order_numbers) != set(range(1, len(images) + 1)):
                    print(f"Error: Please use each number from 1 to {len(images)} exactly once.")
                    continue

                ordered_images = [images[i - 1] for i in order_numbers]

                print("\nNew order:")
                for i, img_path in enumerate(ordered_images, 1):
                    filename = os.path.basename(img_path)
                    print(f"{i:2d}. {filename}")

                confirm = input("\nConfirm this order? (y/n): ").strip().lower()
                if confirm in ["y", "yes"]:
                    return ordered_images
                else:
                    print("Let's try again...")
                    continue

            except ValueError:
                print("Error: Please enter only numbers separated by spaces.")

    def convert_to_pdf(
        self,
        images: List[str],
        output_path: Union[str, Path],
        max_size: int = 2000,
        resolution: float = 100.0
    ) -> bool:
        """
        Convert a list of images to a single PDF file.

        Args:
            images: List of image file paths to convert.
            output_path: Path for the output PDF file.
            max_size: Maximum dimension (width or height) for image resizing.
                Images larger than this will be scaled down. Defaults to 2000.
            resolution: PDF resolution in DPI. Defaults to 100.0.

        Returns:
            True if conversion was successful, False otherwise.

        Raises:
            ValueError: If no images are provided.

        Example:
            >>> converter = ImageToPDFConverter()
            >>> success = converter.convert_to_pdf(
            ...     ["photo1.jpg", "photo2.png"],
            ...     "album.pdf"
            ... )
        """
        if not images:
            print("No images found!")
            return False

        output_path = Path(output_path)
        if not output_path.suffix.lower() == ".pdf":
            output_path = output_path.with_suffix(".pdf")

        try:
            pdf_images: List[Image.Image] = []
            print(f"\nProcessing {len(images)} images...")

            for i, img_path in enumerate(images, 1):
                print(f"Processing image {i}/{len(images)}: {os.path.basename(img_path)}")

                with Image.open(img_path) as img:
                    # Convert to RGB if necessary (required for PDF)
                    if img.mode != "RGB":
                        img = img.convert("RGB")

                    # Resize if too large
                    if max(img.width, img.height) > max_size:
                        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

                    pdf_images.append(img.copy())

            if pdf_images:
                # Ensure output directory exists
                output_path.parent.mkdir(parents=True, exist_ok=True)

                pdf_images[0].save(
                    str(output_path),
                    save_all=True,
                    append_images=pdf_images[1:],
                    format="PDF",
                    resolution=resolution
                )

                print(f"\n✅ PDF created successfully: {output_path}")
                print(f"📄 Total pages: {len(pdf_images)}")
                return True

        except FileNotFoundError as e:
            print(f"❌ Error: Image file not found: {e}")
            return False
        except PermissionError as e:
            print(f"❌ Error: Permission denied: {e}")
            return False
        except Exception as e:
            print(f"❌ Error creating PDF: {e}")
            return False

        return False

    def run(
        self,
        input_paths: Union[str, Path, List[Union[str, Path]]],
        output_path: Optional[Union[str, Path]] = None
    ) -> bool:
        """
        Run the complete conversion workflow.

        This method provides an interactive experience for converting images to PDF,
        including image discovery, ordering, and output path selection.

        Args:
            input_paths: Input image files or directories to process.
            output_path: Optional output PDF path. If not provided, user will be prompted.

        Returns:
            True if conversion was successful, False otherwise.
        """
        print("🖼️  Image to PDF Converter")
        print("=" * 40)

        # Find images
        if isinstance(input_paths, (str, Path)):
            images = self.find_images(input_paths)
        else:
            all_images: List[str] = []
            for path in input_paths:
                all_images.extend(self.find_images(path))
            images = sorted(set(all_images))

        if not images:
            print("❌ No supported images found!")
            print(f"Supported formats: {', '.join(sorted(self.supported_formats))}")
            return False

        # Get user ordering preference
        ordered_images = self.get_user_ordering_preference(images)

        # Prompt for output location if not provided
        if not output_path:
            print("\nWhere do you want to save the PDF?")
            print("1. Same location as the first image")
            print("2. Custom location")

            while True:
                choice = input("Enter your choice (1 or 2): ").strip()
                if choice == "1":
                    first_image_dir = Path(ordered_images[0]).parent
                    output_path = first_image_dir / "converted_images.pdf"
                    break
                elif choice == "2":
                    custom_path = input("Enter full path for PDF (including filename): ").strip()
                    if not custom_path.lower().endswith(".pdf"):
                        custom_path += ".pdf"
                    output_path = Path(custom_path)
                    break
                else:
                    print("Invalid choice. Please enter 1 or 2.")

        # Ensure .pdf extension
        output_path = Path(output_path)
        if not output_path.suffix.lower() == ".pdf":
            output_path = output_path.with_suffix(".pdf")

        # Convert
        success = self.convert_to_pdf(ordered_images, output_path)

        if success:
            file_size = output_path.stat().st_size / (1024 * 1024)
            print(f"📁 File size: {file_size:.2f} MB")

        return success
