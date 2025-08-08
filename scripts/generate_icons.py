#!/usr/bin/env python3

"""Generate app icons for different resolutions"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, output_path):
    """Create a simple icon with text"""
    # Create new image with dark background
    img = Image.new('RGBA', (size, size), color=(33, 33, 33, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw circle
    margin = size // 8
    draw.ellipse(
        [margin, margin, size - margin, size - margin],
        fill=(0, 122, 255, 255),
        outline=(255, 255, 255, 255),
        width=2
    )
    
    # Add text
    text = "CH"
    try:
        font_size = size // 3
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # Get text size
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center text
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    
    # Save
    img.save(output_path, 'PNG')
    print(f"Created icon: {output_path}")

def main():
    """Generate all required icon sizes"""
    
    icon_sizes = {
        'ldpi': 36,
        'mdpi': 48,
        'hdpi': 72,
        'xhdpi': 96,
        'xxhdpi': 144,
        'xxxhdpi': 192
    }
    
    base_dir = "src/main/res"
    
    for density, size in icon_sizes.items():
        # Create directory
        dir_path = os.path.join(base_dir, f"drawable-{density}")
        os.makedirs(dir_path, exist_ok=True)
        
        # Generate icon
        icon_path = os.path.join(dir_path, "ic_launcher.png")
        create_icon(size, icon_path)
    
    # Create default icon
    default_dir = os.path.join(base_dir, "drawable")
    os.makedirs(default_dir, exist_ok=True)
    create_icon(48, os.path.join(default_dir, "ic_launcher.png"))
    
    # Create focus and exposure icons
    create_icon(32, os.path.join(default_dir, "ic_focus.png"))
    create_icon(32, os.path.join(default_dir, "ic_exposure.png"))
    
    print("✅ All icons generated successfully!")

if __name__ == "__main__":
    main()
