#!/usr/bin/env python3
"""
Analyze extracted images to make them readable by Copilot.
Uses OCR to extract text from images and creates descriptions.
"""
import os
from pathlib import Path
from PIL import Image
import pytesseract
import json

def analyze_images(images_dir="extracted_content/images", output_file="extracted_content/IMAGE_CONTENT.md"):
    """
    Analyze all extracted images using OCR to extract text content.
    Creates a markdown file with all image text for Copilot to read.
    """
    images_path = Path(images_dir)
    
    if not images_path.exists():
        print(f"Error: Images directory not found: {images_dir}")
        return
    
    # Get all PNG images
    image_files = sorted(images_path.glob("*.png"))
    total_images = len(image_files)
    
    print(f"Analyzing {total_images} images with OCR...")
    
    markdown_lines = []
    markdown_lines.append("# ECM-L Architecture - Image Content Analysis\n\n")
    markdown_lines.append("This document contains text extracted from all diagrams and images using OCR.\n")
    markdown_lines.append("This makes the visual content searchable and readable by Copilot.\n\n")
    markdown_lines.append(f"**Total Images Analyzed**: {total_images}\n\n")
    markdown_lines.append("---\n\n")
    
    # Also create a JSON file with structured data
    image_data = []
    
    images_with_text = 0
    total_text_length = 0
    
    for idx, image_file in enumerate(image_files, 1):
        if idx % 100 == 0:
            print(f"  Processing image {idx}/{total_images}...")
        
        try:
            # Open image
            img = Image.open(image_file)
            
            # Get image info
            width, height = img.size
            
            # Only process images larger than tiny icons (likely to have meaningful content)
            if width > 50 and height > 50:
                # Extract text using OCR
                text = pytesseract.image_to_string(img)
                text = text.strip()
                
                if text and len(text) > 3:  # Only include if substantial text found
                    images_with_text += 1
                    total_text_length += len(text)
                    
                    # Add to markdown
                    markdown_lines.append(f"## {image_file.name}\n\n")
                    markdown_lines.append(f"**Location**: `images/{image_file.name}`\n")
                    markdown_lines.append(f"**Dimensions**: {width}x{height}px\n")
                    markdown_lines.append(f"**File Size**: {image_file.stat().st_size} bytes\n\n")
                    markdown_lines.append("**Extracted Text Content**:\n\n")
                    markdown_lines.append("```\n")
                    markdown_lines.append(text)
                    markdown_lines.append("\n```\n\n")
                    markdown_lines.append("---\n\n")
                    
                    # Add to JSON data
                    image_data.append({
                        "filename": image_file.name,
                        "path": f"images/{image_file.name}",
                        "width": width,
                        "height": height,
                        "text": text,
                        "text_length": len(text)
                    })
        
        except Exception as e:
            print(f"  Warning: Could not process {image_file.name}: {e}")
    
    # Write markdown file
    output_path = Path(output_file)
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(markdown_lines)
    
    print(f"\n✓ Analysis complete!")
    print(f"✓ Images with text content: {images_with_text}/{total_images}")
    print(f"✓ Total text extracted: {total_text_length} characters")
    print(f"✓ Results saved to: {output_path}")
    
    # Write JSON file for structured access
    json_path = output_path.parent / "image_content.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(image_data, f, indent=2)
    
    print(f"✓ JSON data saved to: {json_path}")
    
    return {
        "total_images": total_images,
        "images_with_text": images_with_text,
        "total_text_length": total_text_length,
        "output_file": str(output_path)
    }

if __name__ == "__main__":
    result = analyze_images()
    
    if result:
        print(f"\n✓ Successfully analyzed {result['total_images']} images")
        print(f"✓ Found text in {result['images_with_text']} images")
        print(f"✓ Extracted {result['total_text_length']} characters of text")
