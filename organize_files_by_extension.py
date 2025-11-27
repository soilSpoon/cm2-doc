"""
Organize files in the manuals directory by file extension.
Creates subdirectories for each extension and moves files accordingly.
"""

import os
from glob import glob
from pathlib import Path

manuals_dir = "/workspaces/dronerush/cm2/manuals"

# Create extension to folder name mapping
extension_folders = {
    "pdf": "pdfs",
    "json": "jsons",
    "md": "markdowns"
}

# Create folders
for ext, folder_name in extension_folders.items():
    folder_path = os.path.join(manuals_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    print(f"Created/verified folder: {folder_path}")

# Move files to appropriate folders
for ext, folder_name in extension_folders.items():
    pattern = os.path.join(manuals_dir, f"*.{ext}")
    files = glob(pattern)
    
    for file_path in files:
        filename = os.path.basename(file_path)
        dest_path = os.path.join(manuals_dir, folder_name, filename)
        
        try:
            os.rename(file_path, dest_path)
            print(f"  Moved: {filename} → {folder_name}/")
        except Exception as e:
            print(f"  ✗ Error moving {filename}: {e}")

print("\nFile organization complete!")

