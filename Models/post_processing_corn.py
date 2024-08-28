import numpy as np
from corn_data import CornData

class PostprocessingCorn:
    
    def __init__(self,corndata:CornData):
        self.corndata = corndata
    
    @staticmethod
    def _calculate_iou(mask1, mask2):
        # Function to calculate Intersection over Union (IoU) between two masks
        intersection = np.logical_and(mask1, mask2).sum()
        union = np.logical_or(mask1, mask2).sum()
        return intersection / union

    def check_iou_area(self, upperband=1, lowerband=0.4):
        
        delete_ids = set()
        
        for i in range(self.corndata.mask_size):
                      
            if any([
                self.corndata.masks[i]['area'] >= 10000,
                self.corndata.masks[i]['area'] < 1000,
                self.corndata.masks[i]['predicted_iou'] <= 0.93,
                self.corndata.masks[i]['stability_score'] <= 0.93
            ]):
                delete_ids.add(i)
                continue  # Skip to the next iteration
            
            for j in range(i + 1, self.corndata.mask_size):
                if j in delete_ids:  # Skip if j is already marked for deletion
                    continue
                
                iou = PostprocessingCorn._calculate_iou(self.corndata.masks[i]['segmentation'], self.corndata.masks[j]['segmentation'])
            
                if lowerband <= iou <= upperband:
                    delete_ids.add(i if self.corndata.masks[i]['area'] >= self.corndata.masks[j]['area'] else j)
    
        keep_ids = list(set(range(self.corndata.mask_size)) - delete_ids)  # indices that are not in delete_ids
        
        self.corndata.valid_mask_id = keep_ids # List of indices that are not in delete_ids
        self.corndata.filterd_mask = [self.corndata.masks[i] for i in self.corndata.valid_mask_id]


    def calculate_center_bondingbox(self):
        for i in range(0,self.corndata.mask_size):
                    x = self.corndata.masks[i]['bbox'][0] + (self.corndata.masks[i]['bbox'][2]/2)
                    y = self.corndata.masks[i]['bbox'][1] + (self.corndata.masks[i]['bbox'][3]/2)
                    self.corndata.masks[i]['centroid'] = (x,y)