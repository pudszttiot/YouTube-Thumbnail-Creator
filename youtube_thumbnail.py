#!/usr/bin/env python3
"""
YouTube Thumbnail Converter

Converts any image by stretching it exactly to 1280x720 pixels
"""

import os
import sys
from PIL import Image
import io

# Import colorama for colored terminal text
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    # Fallback if colorama not installed: define dummy Fore and Style
    class Dummy:
        RESET_ALL = ''
        RED = ''
        GREEN = ''
        YELLOW = ''
        CYAN = ''
        MAGENTA = ''
        BRIGHT = ''
    Fore = Style = Dummy()

def prompt_input_or_quit(prompt):
    """
    Prompts the user for input with the given prompt string.
    If the user enters 'q' or 'quit', the program will exit gracefully.
    Returns the user input string otherwise.
    """
    user_input = input(prompt).strip()
    if user_input.lower() in ['q', 'quit']:
        print()
        print(f"{Fore.MAGENTA}Program exited by user.{Style.RESET_ALL}")
        print()
        sys.exit(0)
    return user_input


def main():
    print()
    print(f"{Fore.MAGENTA}YouTube Thumbnail Converter (1280x720){Style.RESET_ALL}")
    # Display initial instructions about quitting
    print(f"{Fore.YELLOW}Tip: Type 'q' or 'quit' at any prompt to exit the program.{Style.RESET_ALL}")
    print()  # Blank line

    # Prompt for input filename with quit option
    input_path = prompt_input_or_quit(f"{Fore.CYAN}Enter the input image file name with extension (png, jpg, etc.): {Style.RESET_ALL}")
    while not input_path:
        print(f"{Fore.RED}Input file name cannot be empty.{Style.RESET_ALL}")
        print()
        input_path = prompt_input_or_quit(f"{Fore.CYAN}Enter the input image file name with extension (png, jpg, etc.): {Style.RESET_ALL}")

    print()  # Blank line

    output_path = prompt_input_or_quit(f"{Fore.CYAN}Enter the output file name (press Enter to use default): {Style.RESET_ALL}")
    print()

    # Initialize converter and convert
    class YouTubeThumbnailConverter:
        def __init__(self):
            self.target_width = 1280
            self.target_height = 720
            self.max_file_size = 2 * 1024 * 1024  # 2MB in bytes
            self.min_width = 640

        def resize_image_stretch(self, image):
            """
            Resize the image by stretching to exactly 1280x720 pixels
            """
            stretched_image = image.resize((self.target_width, self.target_height), Image.Resampling.LANCZOS)
            return stretched_image

        def optimize_file_size(self, image, output_path, max_quality=95, min_quality=60):
            """Optimize image quality to stay under file size limit"""
            quality = max_quality
            while quality >= min_quality:
                buffer = io.BytesIO()
                image.save(buffer, format='JPEG', quality=quality, optimize=True)
                file_size = buffer.tell()
                if file_size <= self.max_file_size:
                    buffer.seek(0)
                    with open(output_path, 'wb') as f:
                        f.write(buffer.getvalue())
                    return quality, file_size
                quality -= 5
            # Save anyway if quality bounds exhausted
            buffer.seek(0)
            with open(output_path, 'wb') as f:
                f.write(buffer.getvalue())
            return quality, file_size

        def convert_image(self, input_path, output_path=None):
            try:
                if not os.path.exists(input_path):
                    print(f"{Fore.RED}Error: Input file not found: {input_path}{Style.RESET_ALL}")
                    return None
                if output_path is None or output_path.strip() == '':
                    name, _ = os.path.splitext(input_path)
                    output_path = f"{name}_youtube_thumbnail.jpg"

                with Image.open(input_path) as img:
                    if img.mode != 'RGB':
                        img = img.convert('RGB')

                    original_size = img.size
                    print(f"{Fore.CYAN}Original image size: {original_size[0]}x{original_size[1]}{Style.RESET_ALL}")
                    print()

                    if original_size[0] < self.min_width:
                        print(f"{Fore.YELLOW}Warning: Image width ({original_size[0]}px) is below YouTube's minimum requirement ({self.min_width}px){Style.RESET_ALL}")
                        print()

                    processed_image = self.resize_image_stretch(img)
                    print(f"{Fore.CYAN}Processed image size: {processed_image.size[0]}x{processed_image.size[1]}{Style.RESET_ALL}")
                    print()

                    quality, file_size = self.optimize_file_size(processed_image, output_path)
                    file_size_mb = file_size / (1024 * 1024)
                    print(f"{Fore.GREEN}Output saved to: {output_path}{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}Final file size: {file_size_mb:.2f}MB (Quality: {quality}%) {Style.RESET_ALL}")
                    print()

                    if file_size > self.max_file_size:
                        print(f"{Fore.YELLOW}Warning: File size exceeds 2MB limit. Consider using a smaller input image.{Style.RESET_ALL}")
                        print()

                    return output_path

            except Exception as e:
                print(f"{Fore.RED}Error processing image: {str(e)}{Style.RESET_ALL}")
                print()
                return None

    converter = YouTubeThumbnailConverter()
    result = converter.convert_image(input_path, output_path)

    if result:
        print(f"{Fore.GREEN}✅ Conversion successful!{Style.RESET_ALL}")
        print()
    else:
        print(f"{Fore.RED}❌ Conversion failed!{Style.RESET_ALL}")
        print()
        sys.exit(1)

if __name__ == "__main__":
    main()