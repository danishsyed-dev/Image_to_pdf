

import os
import sys
from PIL import Image
import pillow_heif
import argparse

# Register HEIF opener with Pillow
pillow_heif.register_heif_opener()

class ImageToPDFConverter:
    def __init__(self):
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.webp', '.heic', '.heif', '.bmp', '.tiff', '.tif'}

    def find_images(self, directory_or_files):
        images = []
        if isinstance(directory_or_files, str):
            if os.path.isdir(directory_or_files):
                for file in os.listdir(directory_or_files):
                    file_path = os.path.join(directory_or_files, file)
                    if os.path.isfile(file_path):
                        _, ext = os.path.splitext(file.lower())
                        if ext in self.supported_formats:
                            images.append(file_path)
            elif os.path.isfile(directory_or_files):
                _, ext = os.path.splitext(directory_or_files.lower())
                if ext in self.supported_formats:
                    images.append(directory_or_files)
        else:
            for item in directory_or_files:
                if os.path.isfile(item):
                    _, ext = os.path.splitext(item.lower())
                    if ext in self.supported_formats:
                        images.append(item)
                elif os.path.isdir(item):
                    for file in os.listdir(item):
                        file_path = os.path.join(item, file)
                        if os.path.isfile(file_path):
                            _, ext = os.path.splitext(file.lower())
                            if ext in self.supported_formats:
                                images.append(file_path)
        return sorted(images)

    def display_images_with_numbers(self, images):
        print("\n" + "="*60)
        print("FOUND IMAGES:")
        print("="*60)
        for i, img_path in enumerate(images, 1):
            filename = os.path.basename(img_path)
            print(f"{i:2d}. {filename}")
        print("="*60)

    def get_user_ordering_preference(self, images):
        self.display_images_with_numbers(images)
        print("\nHow would you like to arrange these images in the PDF?")
        print("1. Default order (as listed above)")
        print("2. Custom order (specify by numbers)")
        while True:
            choice = input("\nEnter your choice (1 or 2): ").strip()
            if choice == '1':
                return images
            elif choice == '2':
                return self.get_custom_order(images)
            else:
                print("Invalid choice. Please enter 1 or 2.")

    def get_custom_order(self, images):
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
                ordered_images = [images[i-1] for i in order_numbers]
                print("\nNew order:")
                for i, img_path in enumerate(ordered_images, 1):
                    filename = os.path.basename(img_path)
                    print(f"{i:2d}. {filename}")
                confirm = input("\nConfirm this order? (y/n): ").strip().lower()
                if confirm in ['y', 'yes']:
                    return ordered_images
                else:
                    print("Let's try again...")
                    continue
            except ValueError:
                print("Error: Please enter only numbers separated by spaces.")
            except Exception as e:
                print(f"Error: {e}")

    def convert_to_pdf(self, images, output_path):
        if not images:
            print("No images found!")
            return False
        try:
            pdf_images = []
            print(f"\nProcessing {len(images)} images...")
            for i, img_path in enumerate(images, 1):
                print(f"Processing image {i}/{len(images)}: {os.path.basename(img_path)}")
                with Image.open(img_path) as img:
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    max_size = 2000
                    if max(img.width, img.height) > max_size:
                        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                    pdf_images.append(img.copy())
            if pdf_images:
                pdf_images[0].save(
                    output_path,
                    save_all=True,
                    append_images=pdf_images[1:],
                    format='PDF',
                    resolution=100.0
                )
                print(f"\n✅ PDF created successfully: {output_path}")
                print(f"📄 Total pages: {len(pdf_images)}")
                return True
        except Exception as e:
            print(f"❌ Error creating PDF: {e}")
            return False

    def run(self, input_paths, output_path=None):
        print("🖼️  Image to PDF Converter")
        print("=" * 40)
        if isinstance(input_paths, str):
            images = self.find_images(input_paths)
        else:
            all_images = []
            for path in input_paths:
                all_images.extend(self.find_images(path))
            images = sorted(set(all_images))
        if not images:
            print("❌ No supported images found!")
            print(f"Supported formats: {', '.join(self.supported_formats)}")
            return False
        ordered_images = self.get_user_ordering_preference(images)
        # Prompt for output location if not provided
        if not output_path:
            print("\nWhere do you want to save the PDF?")
            print("1. Same location as the first image")
            print("2. Custom location")
            while True:
                choice = input("Enter your choice (1 or 2): ").strip()
                if choice == '1':
                    first_image_dir = os.path.dirname(ordered_images[0])
                    output_path = os.path.join(first_image_dir, "converted_images.pdf")
                    break
                elif choice == '2':
                    custom_path = input("Enter full path for PDF (including filename): ").strip()
                    if not custom_path.lower().endswith('.pdf'):
                        custom_path += '.pdf'
                    output_path = custom_path
                    break
                else:
                    print("Invalid choice. Please enter 1 or 2.")
        if not output_path.lower().endswith('.pdf'):
            output_path += '.pdf'
        success = self.convert_to_pdf(ordered_images, output_path)
        if success:
            file_size = os.path.getsize(output_path) / (1024 * 1024)
            print(f"📁 File size: {file_size:.2f} MB")
        return success

def main():
    parser = argparse.ArgumentParser(description='Convert images to PDF with custom ordering')
    parser.add_argument('inputs', nargs='+', help='Input images or directories')
    parser.add_argument('-o', '--output', help='Output PDF filename', default='converted_images.pdf')
    args = parser.parse_args()
    converter = ImageToPDFConverter()
    converter.run(args.inputs, args.output)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("🖼️  Interactive Image to PDF Converter")
        print("=" * 40)
        input_path = input("Enter image file(s) or directory path: ").strip()
        if not input_path:
            print("❌ No input provided!")
            sys.exit(1)
        if ' ' in input_path:
            input_paths = [path.strip('"').strip("'") for path in input_path.split()]
        else:
            input_paths = input_path.strip('"').strip("'")
        output_path = input("Enter output PDF filename (press Enter for 'converted_images.pdf'): ").strip()
        if not output_path:
            output_path = "converted_images.pdf"
        converter = ImageToPDFConverter()
        converter.run(input_paths, output_path)
    else:
        main()