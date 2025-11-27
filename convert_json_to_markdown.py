"""
Convert JSON files from Upstage document parsing to Markdown files.
Each JSON file contains parsed document structure with markdown content.
"""

from glob import glob
import json
import os

def convert_json_to_markdown(json_file, output_file):
    """Convert a JSON file from Upstage document parsing to Markdown."""
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    markdown_lines = []
    
    # Extract document metadata if available
    if "model" in data:
        markdown_lines.append(f"<!-- Model: {data['model']} -->\n\n")
    
    # Group elements by page
    elements = data.get("elements", [])
    if not elements:
        print(f"  Warning: No elements found in {json_file}")
        return
    
    # Group by page number
    pages_dict = {}
    for element in elements:
        page_num = element.get("page", 1)
        if page_num not in pages_dict:
            pages_dict[page_num] = []
        pages_dict[page_num].append(element)
    
    # Process pages in order
    sorted_pages = sorted(pages_dict.keys())
    for page_num in sorted_pages:
        # Add page separator
        if page_num > sorted_pages[0]:
            markdown_lines.append("\n\n---\n\n")
        
        markdown_lines.append(f"<!-- Page {page_num} -->\n\n")
        
        # Process elements in the page
        for element in pages_dict[page_num]:
            category = element.get("category", "")
            content = element.get("content", {})
            markdown_content = content.get("markdown", "")
            
            if markdown_content:
                # Add the markdown content
                markdown_lines.append(markdown_content)
                # Add spacing after each element
                if not markdown_content.endswith("\n"):
                    markdown_lines.append("\n")
                markdown_lines.append("\n")
    
    # Write to markdown file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("".join(markdown_lines))

# Find all JSON files in the manuals directory
manuals_dir = "/workspaces/dronerush/cm2/manuals"
json_files = glob(os.path.join(manuals_dir, "*.json"))

# Convert each JSON file to Markdown
print(f"Found {len(json_files)} JSON file(s) to convert")
for json_file in json_files:
    print(f"Converting: {json_file}")
    output_file = os.path.splitext(json_file)[0] + ".md"
    try:
        convert_json_to_markdown(json_file, output_file)
        print(f"  ✓ Successfully converted: {output_file}")
    except Exception as e:
        print(f"  ✗ Error converting {json_file}: {e}")
        import traceback
        traceback.print_exc()

print("All files converted.")

