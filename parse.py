"""
Requirements: `pip install requests`
"""
 
from glob import glob
import json
import os
import requests
 
API_KEY = os.environ.get('API_KEY')
 
def call_document_parse(input_file, output_file):
    # Send request
    # output_formats: Request both markdown and html formats
    # base64_encoding: Include base64 encoding for figure category images
    response = requests.post(
        "https://api.upstage.ai/v1/document-digitization",
        headers={"Authorization": f"Bearer {API_KEY}"},
        data={
            "output_formats": '["markdown", "html", "text"]',  # Request both markdown and html
            "model": "document-parse",
        },
        files={"document": open(input_file, "rb")})
 
    # Save response
    if response.status_code == 200:
        with open(output_file, "w") as f:
            json.dump(response.json(), f, ensure_ascii=False)
    else:
        raise ValueError(f"Unexpected status code {response.status_code}.")
 
# Find all PDF files in the pdfs subdirectory
manuals_dir = "/workspaces/dronerush/cm2/manuals/"
pdfs_dir = os.path.join(manuals_dir, "pdfs")
jsons_dir = os.path.join(manuals_dir, "jsons")

# Create jsons directory if it doesn't exist
os.makedirs(jsons_dir, exist_ok=True)

# Find all PDF files in the pdfs directory
pdf_files = glob(os.path.join(pdfs_dir, "*.pdf"))

# Send request and save response for all PDF files
print(f"Found {len(pdf_files)} PDF file(s) to process")
for input_file in pdf_files:
    print(f"Processing: {input_file}")
    # Get the base filename without extension
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    # Save JSON file in jsons directory
    output_file = os.path.join(jsons_dir, f"{base_name}.json")
    try:
        call_document_parse(input_file, output_file)
        print(f"  ✓ Successfully processed: {output_file}")
    except Exception as e:
        print(f"  ✗ Error processing {input_file}: {e}")
print("All files processed.")