#!/usr/bin/env python3
"""
Extract all content from ECM-L Architecture PDF including text, images, and diagrams.
"""
import fitz  # PyMuPDF
import os
import sys
from pathlib import Path

def extract_pdf_content(pdf_path, output_dir="extracted_content"):
    """
    Extract all content from PDF including text, images, and structure.
    
    Args:
        pdf_path: Path to the PDF file
        output_dir: Directory to save extracted content
    """
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Create images subdirectory
    images_path = output_path / "images"
    images_path.mkdir(exist_ok=True)
    
    # Open PDF
    print(f"Opening PDF: {pdf_path}")
    doc = fitz.open(pdf_path)
    
    # Prepare markdown output
    markdown_lines = []
    markdown_lines.append(f"# ECM-L Architecture Documentation\n")
    markdown_lines.append(f"Extracted from: {Path(pdf_path).name}\n")
    markdown_lines.append(f"Total Pages: {len(doc)}\n")
    markdown_lines.append(f"---\n\n")
    
    # Extract metadata
    metadata = doc.metadata
    if metadata:
        markdown_lines.append("## Document Metadata\n\n")
        for key, value in metadata.items():
            if value:
                markdown_lines.append(f"- **{key}**: {value}\n")
        markdown_lines.append("\n---\n\n")
    
    # Process each page
    image_counter = 0
    for page_num in range(len(doc)):
        page = doc[page_num]
        print(f"Processing page {page_num + 1}/{len(doc)}...")
        
        markdown_lines.append(f"## Page {page_num + 1}\n\n")
        
        # Extract text
        text = page.get_text()
        if text.strip():
            markdown_lines.append(text)
            markdown_lines.append("\n")
        
        # Extract images
        image_list = page.get_images()
        if image_list:
            markdown_lines.append(f"\n### Images on Page {page_num + 1}\n\n")
            
        for img_index, img in enumerate(image_list):
            xref = img[0]
            try:
                # Extract image
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                # Save image
                image_counter += 1
                image_filename = f"page_{page_num + 1:03d}_image_{img_index + 1:02d}.{image_ext}"
                image_path = images_path / image_filename
                
                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)
                
                print(f"  Extracted image: {image_filename}")
                
                # Add reference in markdown
                markdown_lines.append(f"![Image {image_counter}](images/{image_filename})\n\n")
                markdown_lines.append(f"*Image {image_counter}: Extracted from page {page_num + 1}*\n\n")
                
            except Exception as e:
                print(f"  Error extracting image {img_index}: {e}")
        
        # Extract drawings/vector graphics information
        drawings = page.get_drawings()
        if drawings:
            markdown_lines.append(f"\n### Vector Graphics on Page {page_num + 1}\n\n")
            markdown_lines.append(f"*This page contains {len(drawings)} vector graphic elements (diagrams, shapes, lines)*\n\n")
        
        markdown_lines.append("\n---\n\n")
    
    # Write markdown file
    markdown_file = output_path / "ECM-L_Architecture.md"
    with open(markdown_file, "w", encoding="utf-8") as f:
        f.writelines(markdown_lines)
    
    print(f"\nExtraction complete!")
    print(f"- Markdown file: {markdown_file}")
    print(f"- Total images extracted: {image_counter}")
    print(f"- Images directory: {images_path}")
    
    # Create a summary file
    summary_file = output_path / "EXTRACTION_SUMMARY.md"
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write("# ECM-L Architecture PDF Extraction Summary\n\n")
        f.write(f"## Source File\n")
        f.write(f"- **File**: {Path(pdf_path).name}\n")
        f.write(f"- **Pages**: {len(doc)}\n")
        f.write(f"- **Images Extracted**: {image_counter}\n\n")
        f.write(f"## Output Files\n\n")
        f.write(f"- **Main Document**: [ECM-L_Architecture.md](ECM-L_Architecture.md)\n")
        f.write(f"- **Images Directory**: [images/](images/)\n\n")
        f.write(f"## Contents\n\n")
        f.write(f"The main document contains:\n")
        f.write(f"- Full text content from all pages\n")
        f.write(f"- All extracted images with references\n")
        f.write(f"- Document metadata\n")
        f.write(f"- Page structure and organization\n\n")
        f.write(f"## Usage\n\n")
        f.write(f"You can now ask Copilot questions about the ECM-L architecture by referencing ")
        f.write(f"the extracted content in `ECM-L_Architecture.md` and the images in the `images/` directory.\n")
    
    print(f"- Summary file: {summary_file}")
    
    # Store page count before closing
    total_pages = len(doc)
    doc.close()
    
    return {
        "markdown_file": str(markdown_file),
        "images_count": image_counter,
        "pages": total_pages
    }

if __name__ == "__main__":
    # The PDF file uploaded today (Feb 4, 2026)
    pdf_file = "Enterprise Correspondence Manage_a625210899d84ccbb5ad17e999a126b3-040226-1933-2402.pdf"
    
    if not os.path.exists(pdf_file):
        print(f"Error: PDF file not found: {pdf_file}")
        sys.exit(1)
    
    result = extract_pdf_content(pdf_file)
    print(f"\n✓ Successfully extracted content from PDF")
    print(f"✓ {result['pages']} pages processed")
    print(f"✓ {result['images_count']} images extracted")
