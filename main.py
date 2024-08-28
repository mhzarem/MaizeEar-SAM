import sys
import os
sys.path.append("./utils")
sys.path.append("./Models")

import concurrent.futures
from corn_path_finder import CornPathFinder
from segment_any_corn import SegmentAnyCorn
from post_processing_corn import PostprocessingCorn
from corn_data import CornData

HYBRID_FOLDER_PATH = "./Data/hybrid_maize/Croped"
MAX_THREADS = 10 


def get_image_paths(root_folder):
    # List of image extensions
    image_extensions = ['.png']
    
    # List to store image paths
    maize_ear_image_paths = []

    # Walk through the directory
    for subdir, _, files in os.walk(root_folder):
        for file in files:
            # Check if the file is an image
            if any(file.lower().endswith(ext) for ext in image_extensions):
                # Add the file path to the list
                maize_ear_image_paths.append(os.path.join(subdir, file))
    
    return maize_ear_image_paths

# Process the image
def process_image(image_path):

    dir_path = os.path.dirname(image_path)
    file_name = os.path.basename(image_path).split(".")[0]
    pkl_path = os.path.join(dir_path, file_name + ".pkl")

    if os.path.exists(pkl_path):
        print(f"Skipping {image_path}")
        return
    else:
        # Load the image
        data = CornData(image_path)
        
        # Segment each kernel of corn by using SAM model
        seg = SegmentAnyCorn(data, checkpoint="./Models/saved_weight/sam_vit_h_4b8939.pth")
        seg.instance_segmention_of_cob()
        
        # Apply post processing on the segmented image
        post = PostprocessingCorn(data)
        post.check_iou_area()
        post.calculate_center_bondingbox()
        
        # Find the path of the corn ear after post processing
        path = CornPathFinder(data)
        path.make_path()
        

        # Save the data to a file
        data.save_to_file(pkl_path)

if __name__ == "__main__":
    image_paths = get_image_paths(HYBRID_FOLDER_PATH)
    print(f"Found {len(image_paths)} Maize ear images")
    print("Processing the images")
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        # Map the process_image function to the list of image_paths
        executor.map(process_image, image_paths)
    

    print("Done processing all images")