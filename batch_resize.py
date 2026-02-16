#!/usr/bin/env python3
"""
Batch image resizer for cake printing
Automatically processes all images in the 'input' directory
"""

from PIL import Image
import os
import glob

def resize_image_for_cake(input_path, output_dir, max_width=2400, max_height=3000, quality=95):
    """
    Resize an image to fit cake printing requirements
    """
    try:
        # Open the image
        img = Image.open(input_path)
        
        print(f"\nProcessing: {os.path.basename(input_path)}")
        print(f"  Original: {img.size[0]}x{img.size[1]} pixels ({os.path.getsize(input_path) / 1024:.2f} KB)")
        
        # Calculate aspect ratio
        aspect_ratio = img.size[0] / img.size[1]
        
        # Calculate new dimensions maintaining aspect ratio
        if aspect_ratio > max_width / max_height:
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:
            new_height = max_height
            new_width = int(max_height * aspect_ratio)
        
        # Resize with high-quality resampling
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert to RGB if necessary (for JPEG)
        if resized_img.mode in ('RGBA', 'P'):
            background = Image.new('RGB', resized_img.size, (255, 255, 255))
            if resized_img.mode == 'RGBA':
                background.paste(resized_img, mask=resized_img.split()[3])
            else:
                background.paste(resized_img)
            resized_img = background
        
        # Create output filename
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(output_dir, f"{base_name}_cake.jpg")
        
        # Save the resized image
        resized_img.save(output_path, 'JPEG', quality=quality, optimize=True)
        
        print(f"  Resized: {new_width}x{new_height} pixels ({os.path.getsize(output_path) / 1024:.2f} KB)")
        print(f"  Cake size: ~{new_width/300:.1f}\" x {new_height/300:.1f}\" (at 300 DPI)")
        print(f"  Saved to: {output_path}")
        
        return output_path
        
    except Exception as e:
        print(f"  Error processing {input_path}: {str(e)}")
        return None

def main():
    input_dir = "input"
    output_dir = "output"
    
    # Create directories if they don't exist
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all image files
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.webp',
                       '*.JPG', '*.JPEG', '*.PNG', '*.GIF', '*.BMP', '*.WEBP']
    
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(input_dir, ext)))
    
    if not image_files:
        print(f"No images found in '{input_dir}/' directory")
        print(f"\nPlace your images in the '{input_dir}/' folder and run this script again.")
        return
    
    print(f"Found {len(image_files)} image(s) to process:")
    print("="*60)
    
    success_count = 0
    for image_file in image_files:
        result = resize_image_for_cake(image_file, output_dir)
        if result:
            success_count += 1
    
    print("\n" + "="*60)
    print(f"Processed {success_count}/{len(image_files)} images successfully")
    print(f"Resized images saved to '{output_dir}/' directory")

if __name__ == "__main__":
    main()
