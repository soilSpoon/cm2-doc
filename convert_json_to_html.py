"""
Convert JSON files from Upstage document parsing to HTML files.
Each JSON file contains parsed document structure with HTML content.
"""

from glob import glob
import json
import os

def convert_json_to_html(json_file, output_file):
    """Convert a JSON file from Upstage document parsing to HTML."""
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    html_parts = []
    
    # Add HTML document structure
    html_parts.append("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }
        .page {
            page-break-after: always;
            margin-bottom: 50px;
            padding: 20px;
            border: 1px solid #ddd;
        }
        .page-header {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 20px;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #333;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 10px 0;
        }
        table td, table th {
            border: 1px solid #ddd;
            padding: 8px;
        }
        pre, code {
            background-color: #f4f4f4;
            padding: 2px 4px;
            border-radius: 3px;
        }
        pre {
            padding: 10px;
            overflow-x: auto;
        }
    </style>
</head>
<body>
""")
    
    # Extract document metadata if available
    if "model" in data:
        html_parts.append(f"<!-- Model: {data['model']} -->\n")
    
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
        html_parts.append(f'<div class="page">\n')
        html_parts.append(f'<div class="page-header">Page {page_num}</div>\n')
        
        # Process elements in the page
        for element in pages_dict[page_num]:
            category = element.get("category", "")
            content = element.get("content", {})
            html_content = content.get("html", "")
            
            if html_content:
                # Add the HTML content
                html_parts.append(html_content)
                html_parts.append("\n")
        
        html_parts.append('</div>\n')
    
    # Close HTML document
    html_parts.append("""
</body>
</html>
""")
    
    # Write to HTML file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("".join(html_parts))

# Find all JSON files in the jsons directory
manuals_dir = "/workspaces/dronerush/cm2/manuals/"
jsons_dir = os.path.join(manuals_dir, "jsons")
htmls_dir = os.path.join(manuals_dir, "htmls")

# Create htmls directory if it doesn't exist
os.makedirs(htmls_dir, exist_ok=True)

# Find all JSON files in the jsons directory
json_files = glob(os.path.join(jsons_dir, "*.json"))

# Convert each JSON file to HTML
print(f"Found {len(json_files)} JSON file(s) to convert")
for json_file in json_files:
    print(f"Converting: {json_file}")
    # Get the base filename without extension
    base_name = os.path.splitext(os.path.basename(json_file))[0]
    # Save HTML file in htmls directory
    output_file = os.path.join(htmls_dir, f"{base_name}.html")
    try:
        convert_json_to_html(json_file, output_file)
        print(f"  ✓ Successfully converted: {output_file}")
    except Exception as e:
        print(f"  ✗ Error converting {json_file}: {e}")
        import traceback
        traceback.print_exc()

print("All files converted.")

