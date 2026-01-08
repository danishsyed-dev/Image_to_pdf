"""
Unit tests for the ImageToPDFConverter class.
"""

import os
import tempfile
from pathlib import Path

import pytest
from PIL import Image

from image_to_pdf.converter import ImageToPDFConverter


@pytest.fixture
def converter():
    """Create a converter instance for testing."""
    return ImageToPDFConverter()


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_images(temp_dir):
    """Create sample test images."""
    images = []
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # RGB colors

    for i, color in enumerate(colors, 1):
        img_path = temp_dir / f"test_image_{i}.png"
        img = Image.new("RGB", (100, 100), color)
        img.save(img_path)
        images.append(str(img_path))

    return images


class TestImageToPDFConverterInit:
    """Tests for ImageToPDFConverter initialization."""

    def test_supported_formats(self, converter):
        """Test that all expected formats are supported."""
        expected = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif", ".bmp", ".tiff", ".tif"}
        assert converter.supported_formats == expected

    def test_instance_creation(self, converter):
        """Test that converter is properly instantiated."""
        assert isinstance(converter, ImageToPDFConverter)


class TestFindImages:
    """Tests for the find_images method."""

    def test_find_images_in_directory(self, converter, temp_dir, sample_images):
        """Test finding images in a directory."""
        found = converter.find_images(str(temp_dir))
        assert len(found) == 3
        assert all(f.endswith(".png") for f in found)

    def test_find_images_single_file(self, converter, sample_images):
        """Test finding a single image file."""
        found = converter.find_images(sample_images[0])
        assert len(found) == 1
        assert found[0] == sample_images[0]

    def test_find_images_list_of_files(self, converter, sample_images):
        """Test finding images from a list of files."""
        found = converter.find_images(sample_images[:2])
        assert len(found) == 2

    def test_find_images_empty_directory(self, converter, temp_dir):
        """Test finding images in an empty directory."""
        empty_dir = temp_dir / "empty"
        empty_dir.mkdir()
        found = converter.find_images(str(empty_dir))
        assert len(found) == 0

    def test_find_images_unsupported_format(self, converter, temp_dir):
        """Test that unsupported formats are ignored."""
        # Create a non-image file
        text_file = temp_dir / "document.txt"
        text_file.write_text("not an image")

        found = converter.find_images(str(temp_dir))
        assert len(found) == 0

    def test_find_images_mixed_formats(self, converter, temp_dir):
        """Test finding images with mixed formats."""
        # Create images with different formats
        formats = [".jpg", ".png", ".bmp"]
        for i, ext in enumerate(formats):
            img = Image.new("RGB", (50, 50), (i * 50, i * 50, i * 50))
            img.save(temp_dir / f"image{i}{ext}")

        found = converter.find_images(str(temp_dir))
        assert len(found) == 3

    def test_find_images_returns_sorted(self, converter, temp_dir):
        """Test that found images are returned sorted."""
        for name in ["c_image.png", "a_image.png", "b_image.png"]:
            img = Image.new("RGB", (10, 10), (255, 255, 255))
            img.save(temp_dir / name)

        found = converter.find_images(str(temp_dir))
        filenames = [os.path.basename(f) for f in found]
        assert filenames == sorted(filenames)

    def test_find_images_with_path_object(self, converter, temp_dir, sample_images):
        """Test finding images with Path object input."""
        found = converter.find_images(temp_dir)
        assert len(found) == 3


class TestConvertToPdf:
    """Tests for the convert_to_pdf method."""

    def test_convert_single_image(self, converter, temp_dir, sample_images):
        """Test converting a single image to PDF."""
        output = temp_dir / "output.pdf"
        success = converter.convert_to_pdf([sample_images[0]], output)

        assert success is True
        assert output.exists()
        assert output.stat().st_size > 0

    def test_convert_multiple_images(self, converter, temp_dir, sample_images):
        """Test converting multiple images to PDF."""
        output = temp_dir / "output.pdf"
        success = converter.convert_to_pdf(sample_images, output)

        assert success is True
        assert output.exists()

    def test_convert_empty_list(self, converter, temp_dir):
        """Test converting an empty list of images."""
        output = temp_dir / "output.pdf"
        success = converter.convert_to_pdf([], output)

        assert success is False
        assert not output.exists()

    def test_convert_adds_pdf_extension(self, converter, temp_dir, sample_images):
        """Test that .pdf extension is added if missing."""
        output = temp_dir / "output"  # No extension
        success = converter.convert_to_pdf([sample_images[0]], output)

        assert success is True
        # Check that .pdf was added
        assert (temp_dir / "output.pdf").exists()

    def test_convert_creates_output_directory(self, converter, temp_dir, sample_images):
        """Test that output directory is created if it doesn't exist."""
        output = temp_dir / "subdir" / "nested" / "output.pdf"
        success = converter.convert_to_pdf([sample_images[0]], output)

        assert success is True
        assert output.exists()

    def test_convert_with_rgba_image(self, converter, temp_dir):
        """Test converting an RGBA image (with alpha channel)."""
        # Create RGBA image
        rgba_path = temp_dir / "rgba_image.png"
        img = Image.new("RGBA", (100, 100), (255, 0, 0, 128))
        img.save(rgba_path)

        output = temp_dir / "output.pdf"
        success = converter.convert_to_pdf([str(rgba_path)], output)

        assert success is True
        assert output.exists()

    def test_convert_with_custom_max_size(self, converter, temp_dir):
        """Test converting with custom max size."""
        # Create a large image
        large_path = temp_dir / "large_image.png"
        img = Image.new("RGB", (3000, 3000), (255, 255, 255))
        img.save(large_path)

        output = temp_dir / "output.pdf"
        success = converter.convert_to_pdf([str(large_path)], output, max_size=500)

        assert success is True
        assert output.exists()

    def test_convert_nonexistent_image(self, converter, temp_dir):
        """Test converting a non-existent image file."""
        output = temp_dir / "output.pdf"
        success = converter.convert_to_pdf(["/nonexistent/image.png"], output)

        assert success is False


class TestSupportedFormats:
    """Tests for format support."""

    def test_jpeg_support(self, converter, temp_dir):
        """Test JPEG format support."""
        for ext in [".jpg", ".jpeg"]:
            assert ext in converter.supported_formats

    def test_png_support(self, converter):
        """Test PNG format support."""
        assert ".png" in converter.supported_formats

    def test_webp_support(self, converter):
        """Test WebP format support."""
        assert ".webp" in converter.supported_formats

    def test_heic_support(self, converter):
        """Test HEIC/HEIF format support."""
        assert ".heic" in converter.supported_formats
        assert ".heif" in converter.supported_formats

    def test_bmp_support(self, converter):
        """Test BMP format support."""
        assert ".bmp" in converter.supported_formats

    def test_tiff_support(self, converter):
        """Test TIFF format support."""
        assert ".tiff" in converter.supported_formats
        assert ".tif" in converter.supported_formats
