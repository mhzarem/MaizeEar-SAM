from PIL import Image
from segment_anything import sam_model_registry, SamPredictor
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry
import numpy as np
import torch
import os

from corn_data import CornData

class SegmentAnyCorn:
    
    def __init__(self, corndata: CornData, model_type= 'vit_h', checkpoint='Models/saved_weight/sam_vit_h_4b8939.pth', points_per_batch=10, points_per_side=80):
  
        self.image_path = corndata.image_path
        self.checkpoint = checkpoint
        self.model_type = model_type
        self.points_per_batch = points_per_batch
        self.points_per_side = points_per_side
        self.corndata = corndata
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.corndata.image = self._read_image()

    def _read_image(self):
        try:
            img = Image.open(self.image_path)
        
            # Convert the image to a NumPy array
            image = np.array(img)
            
            # Assign to the instance variable
            self.corndata.image = image
            
        except FileNotFoundError:
            print(f"Error: {self.image_path} not found.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
   
    def instance_segmention_of_cob(self):
        """
        this function use the segment anything model (SAM) to segment diffrent part of the corn ear
        """
        sam = sam_model_registry[self.model_type](checkpoint=self.checkpoint)
        sam.to(self.device)

        predictor = SamPredictor(sam)
        self._read_image()
        predictor.set_image(self.corndata.image)
        # image_embedding = predictor.get_image_embedding().cpu().numpy()
        mask_generator = SamAutomaticMaskGenerator(sam, points_per_batch=self.points_per_batch, points_per_side=self.points_per_side)
        masks = mask_generator.generate(self.corndata.image)
        self.corndata.masks = masks
        print(f"Segmentation is ended for the image in {self.image_path}")
        
        del predictor
        del mask_generator

if __name__ == "__main__":
    # Test the class with a sample image file and segmenting the corn ear
    data = CornData("1_22-A-1585314.png")
    seg = SegmentAnyCorn(data, checkpoint="saved_weight/sam_vit_h_4b8939.pth")
    seg.instance_segmention_of_cob()