# Start from here 
# This code checks whether some prerequisite model weights are installed or not.
import os
import urllib.request

file_name = "sam_vit_h_4b8939.pth"
url = "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth"

if not os.path.exists(file_name):
    print(f"Downloading {file_name}...")
    urllib.request.urlretrieve(url, file_name)
    print(f"Download completed.")
else:
    print(f"File {file_name} already exists, skipping download.")