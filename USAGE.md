# Image to PDF Converter - Usage Instructions

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage Methods

### Method 1: Interactive Mode
Simply run the script without arguments:
```bash
python image_to_pdf_converter.py
```
The script will prompt you for:
- Input files/directory path
- Output PDF filename
- Image arrangement preference

### Method 2: Command Line Mode
```bash
python image_to_pdf_converter.py [images/directory] -o output.pdf
```

## Examples

### Convert all images in a directory:
```bash
python image_to_pdf_converter.py "/path/to/images" -o "my_photos.pdf"
```

### Convert specific images:
```bash
python image_to_pdf_converter.py photo1.jpg photo2.png photo3.heic -o "selected_photos.pdf"
```

### Interactive mode (no arguments):
```bash
python image_to_pdf_converter.py
# Then follow the prompts
```

## Supported Formats
- JPG/JPEG
- PNG
- WEBP
- HEIC/HEIF
- BMP
- TIFF/TIF

## Features
- Automatic image format detection
- User-friendly ordering confirmation
- Image optimization for PDF size
- Error handling and validation
- Progress indicators
