# 🖼️ Image to PDF Converter

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://github.com/danishsyed-dev/image_to_pdf/actions/workflows/ci.yml/badge.svg)](https://github.com/danishsyed-dev/image_to_pdf/actions)

A powerful, user-friendly CLI tool to convert images to PDF with **custom ordering** and **HEIC/HEIF support**.

## ✨ Features

- **Multiple Format Support**: JPG, PNG, WEBP, HEIC/HEIF, BMP, TIFF
- **Custom Ordering**: Arrange images in any order before conversion
- **Interactive Mode**: User-friendly prompts for easy operation
- **CLI Mode**: Scriptable command-line interface for automation
- **Image Optimization**: Automatic resizing for optimal PDF size
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 📦 Installation

### From Source

```bash
git clone https://github.com/danishsyed-dev/image_to_pdf.git
cd image_to_pdf
pip install -e .
```

### Quick Install (pip)

```bash
pip install Pillow pillow-heif
```

## 🚀 Usage

### Command Line Mode

```bash
# Convert all images in a directory
image-to-pdf /path/to/images -o output.pdf

# Convert specific images
image-to-pdf photo1.jpg photo2.png photo3.heic -o album.pdf

# Using Python module directly
python -m image_to_pdf /path/to/images -o output.pdf
```

### Interactive Mode

Run without arguments for an interactive experience:

```bash
image-to-pdf
# or
python -m image_to_pdf
```

The interactive mode will prompt you for:
1. Input files or directory path
2. Output PDF filename
3. Image arrangement preference (default or custom order)

### Programmatic Usage

```python
from image_to_pdf import ImageToPDFConverter

converter = ImageToPDFConverter()

# Find and convert images
images = converter.find_images("/path/to/images")
converter.convert_to_pdf(images, "output.pdf")
```

## 📁 Supported Formats

| Format | Extension |
|--------|-----------|
| JPEG | `.jpg`, `.jpeg` |
| PNG | `.png` |
| WebP | `.webp` |
| HEIC/HEIF | `.heic`, `.heif` |
| BMP | `.bmp` |
| TIFF | `.tiff`, `.tif` |

## ⚙️ Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/danishsyed-dev/image_to_pdf.git
cd image_to_pdf

# Install with dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/ -v
```

### Linting

```bash
ruff check src/ tests/
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Contact

Danish Syed - [@danishsyed-dev](https://github.com/danishsyed-dev)

Project Link: [https://github.com/danishsyed-dev/image_to_pdf](https://github.com/danishsyed-dev/image_to_pdf)
