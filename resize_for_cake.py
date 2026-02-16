#!/usr/bin/env python3
"""
Image resizer for cake printing
Resizes images to optimal dimensions for edible cake printing
"""

from PIL import Image
import sys
import os

def resize_image_for_cake(input_path, output_path=None, max_width=2400, max_height=3000, quality=95):
    """
    Resize an image to fit cake printing requirements
    
    Args:
        input_path: Path to input image
        output_path: Path to save resized image (optional)
        max_width: Maximum width in pixels (default 2400 for 8" at 300 DPI)
        max_height: Maximum height in pixels (default 3000 for 10" at 300 DPI)
        quality: JPEG quality (1-100)
    """
    try:
        # Open the image
        img = Image.open(input_path)
        
        print(f"Original dimensions: {img.size[0]}x{img.size[1]} pixels")
        print(f"Original file size: {os.path.getsize(input_path) / 1024:.2f} KB")
        
        # Calculate aspect ratio
        aspect_ratio = img.size[0] / img.size[1]
        
        # Calculate new dimensions maintaining aspect ratio
        if aspect_ratio > max_width / max_height:
            # Width is the limiting factor
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:
            # Height is the limiting factor
            new_height = max_height
            new_width = int(max_height * aspect_ratio)
        
        # Resize with high-quality resampling
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Determine output path
        if output_path is None:
            name, ext = os.path.splitext(input_path)
            output_path = f"{name}_cake{ext}"
        
        # Convert to RGB if necessary (for JPEG)
        if resized_img.mode in ('RGBA', 'P'):
            # Create white background
            background = Image.new('RGB', resized_img.size, (255, 255, 255))
            if resized_img.mode == 'RGBA':
                background.paste(resized_img, mask=resized_img.split()[3])
            else:
                background.paste(resized_img)
            resized_img = background
        
        # Save the resized image
        resized_img.save(output_path, 'JPEG', quality=quality, optimize=True)
        
        print(f"Resized dimensions: {new_width}x{new_height} pixels")
        print(f"New file size: {os.path.getsize(output_path) / 1024:.2f} KB")
        print(f"Saved to: {output_path}")
        print(f"\nThis image is suitable for a cake approximately {new_width/300:.1f}\" x {new_height/300:.1f}\" at 300 DPI")
        
        return output_path
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python resize_for_cake.py <input_image> [output_image]")
        print("Example: python resize_for_cake.py hot_wheels.jpg")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    
    resize_image_for_cake(input_file, output_file)
