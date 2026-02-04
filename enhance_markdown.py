#!/usr/bin/env python3
"""
Enhance the main markdown file with OCR text from images.
"""
import json
from pathlib import Path

def enhance_markdown_with_ocr():
    """
    Add OCR text content to the main markdown file for images that contain text.
    """
    # Load the OCR results
    json_path = Path("extracted_content/image_content.json")
    
    if not json_path.exists():
        print("Error: image_content.json not found. Run analyze_images.py first.")
        return
    
    with open(json_path, "r", encoding="utf-8") as f:
        image_data = json.load(f)
    
    # Create a lookup dictionary
    image_text_map = {img["filename"]: img["text"] for img in image_data}
    
    print(f"Loaded OCR data for {len(image_text_map)} images with text")
    
    # Read the main markdown file
    main_md_path = Path("extracted_content/ECM-L_Architecture.md")
    
    with open(main_md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # Enhance the markdown
    enhanced_lines = []
    images_enhanced = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        enhanced_lines.append(line)
        
        # Check if this is an image reference line
        if line.strip().startswith("![Image") and "](images/" in line:
            # Extract the filename
            import re
            match = re.search(r'\(images/([^)]+)\)', line)
            if match:
                filename = match.group(1)
                
                # Check if we have OCR text for this image
                if filename in image_text_map:
                    ocr_text = image_text_map[filename]
                    
                    # Skip the next line (the "*Image X: Extracted from page Y*" line)
                    i += 1
                    if i < len(lines):
                        enhanced_lines.append(lines[i])
                    
                    # Add the OCR text content
                    enhanced_lines.append("\n**Image Text Content (OCR)**:\n")
                    enhanced_lines.append("```\n")
                    enhanced_lines.append(ocr_text)
                    enhanced_lines.append("\n```\n")
                    
                    images_enhanced += 1
        
        i += 1
    
    # Write the enhanced markdown
    enhanced_path = Path("extracted_content/ECM-L_Architecture_Enhanced.md")
    
    with open(enhanced_path, "w", encoding="utf-8") as f:
        f.writelines(enhanced_lines)
    
    print(f"✓ Enhanced {images_enhanced} images with OCR text")
    print(f"✓ Enhanced document saved to: {enhanced_path}")
    
    # Update the main file
    with open(main_md_path, "w", encoding="utf-8") as f:
        f.writelines(enhanced_lines)
    
    print(f"✓ Main document updated: {main_md_path}")
    
    return images_enhanced

if __name__ == "__main__":
    count = enhance_markdown_with_ocr()
    print(f"\n✓ Successfully enhanced {count} images with OCR text content")
