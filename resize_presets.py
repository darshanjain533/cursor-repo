#!/usr/bin/env python3
"""
Cake Image Resizer with Presets
Choose from predefined cake sizes
"""

from PIL import Image
import os
import sys
import glob

# Preset cake sizes (in pixels at 300 DPI)
CAKE_PRESETS = {
    '1': {
        'name': 'Small Round (6-8 inches)',
        'width': 2400,
        'height': 2400,
        'description': 'Perfect for small round cakes'
    },
    '2': {
        'name': 'Standard Sheet (8x10 inches)',
        'width': 2400,
        'height': 3000,
        'description': 'Most common cake size - DEFAULT'
    },
    '3': {
        'name': 'Large Round (10-12 inches)',
        'width': 3600,
        'height': 3600,
        'description': 'For larger round celebration cakes'
    },
    '4': {
        'name': 'Quarter Sheet (9x13 inches)',
        'width': 2700,
        'height': 3900,
        'description': 'Quarter sheet cake'
    },
    '5': {
        'name': 'Half Sheet (12x18 inches)',
        'width': 3600,
        'height': 5400,
        'description': 'Half sheet cake for parties'
    },
    '6': {
        'name': 'Square Cake (8x8 inches)',
        'width': 2400,
        'height': 2400,
        'description': 'Square shaped cake'
    }
}

def resize_image(input_path, output_dir, width, height, quality=95):
    """Resize image to specified dimensions"""
    try:
        img = Image.open(input_path)
        
        print(f"\n  📸 Processing: {os.path.basename(input_path)}")
        print(f"     Original: {img.size[0]}x{img.size[1]} pixels")
        
        # Calculate aspect ratio
        aspect_ratio = img.size[0] / img.size[1]
        target_ratio = width / height
        
        # Calculate new dimensions maintaining aspect ratio
        if aspect_ratio > target_ratio:
            new_width = width
            new_height = int(width / aspect_ratio)
        else:
            new_height = height
            new_width = int(height * aspect_ratio)
        
        # Resize with high-quality resampling
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert to RGB if necessary
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
        
        # Save
        resized_img.save(output_path, 'JPEG', quality=quality, optimize=True)
        
        print(f"     Resized: {new_width}x{new_height} pixels")
        print(f"     Size: {os.path.getsize(output_path) / 1024:.1f} KB")
        print(f"     ✅ Saved to: {output_path}")
        
        return output_path
        
    except Exception as e:
        print(f"     ❌ Error: {str(e)}")
        return None

def show_menu():
    """Display cake size menu"""
    print("\n" + "="*60)
    print("🎂 CAKE IMAGE RESIZER - Choose Your Cake Size")
    print("="*60)
    for key, preset in CAKE_PRESETS.items():
        print(f"\n{key}. {preset['name']}")
        print(f"   {preset['description']}")
        print(f"   Dimensions: {preset['width']}x{preset['height']} pixels")

def main():
    input_dir = "input"
    output_dir = "output"
    
    # Create directories
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    # Find images
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.webp',
                       '*.JPG', '*.JPEG', '*.PNG', '*.GIF', '*.BMP', '*.WEBP']
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(input_dir, ext)))
    
    if not image_files:
        print(f"\n❌ No images found in '{input_dir}/' directory")
        print(f"   Place your images there and run again.")
        return
    
    print(f"\n📦 Found {len(image_files)} image(s):")
    for img in image_files:
        print(f"   - {os.path.basename(img)}")
    
    # Show menu
    show_menu()
    
    # Get user choice
    print("\n" + "="*60)
    choice = input("\nChoose cake size (1-6) or press Enter for default [2]: ").strip()
    
    if not choice:
        choice = '2'
    
    if choice not in CAKE_PRESETS:
        print("❌ Invalid choice. Using default (Standard Sheet).")
        choice = '2'
    
    preset = CAKE_PRESETS[choice]
    print(f"\n✅ Selected: {preset['name']}")
    print(f"   {preset['description']}")
    print("\n🔄 Processing images...")
    print("="*60)
    
    # Process images
    success_count = 0
    for image_file in image_files:
        result = resize_image(image_file, output_dir, preset['width'], preset['height'])
        if result:
            success_count += 1
    
    print("\n" + "="*60)
    print(f"✅ Successfully processed {success_count}/{len(image_files)} images")
    print(f"📁 Resized images saved to '{output_dir}/' directory")
    print("="*60)
    print("\n🎉 Ready for your cake printer!")

if __name__ == "__main__":
    main()
