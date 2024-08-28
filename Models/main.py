from corn_data import CornData
from corn_path_finder import CornPathFinder
from corn_path_finder import CornPathFinder
from segment_any_corn import SegmentAnyCorn
from post_processing_corn import PostprocessingCorn
from corn_data import CornData
import matplotlib.pyplot as plt
import sys
sys.path.append("../utils")
from visualization import show_path_on_corn


if __name__ == "__main__":
  
    data = CornData("example_corn.png")
    # segment each kerel of corn by using SAM model
    print("Segmenting the corn ear")
    seg = SegmentAnyCorn(data, checkpoint="saved_weight/sam_vit_h_4b8939.pth")
    seg.instance_segmention_of_cob()
    # Apply post processing on the segmented image
    print("Segmentation is done")
    print("start post processing on the masks")
    post = PostprocessingCorn(data)
    post.check_iou_area()
    post.calculate_center_bondingbox()
    print("Post processing is done")
    print("start finding the path of the corn ear")
    # Find the path of the corn ear after post processing
    path = CornPathFinder(data)
    path.make_path()
    # Visualize the path on the corn image 
    show_path_on_corn(data)
    print("The path is found successfully and visualized on the corn image")

