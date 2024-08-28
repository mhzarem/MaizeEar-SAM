from dataclasses import dataclass, field
import numpy as np 
import pickle

@dataclass
class CornData:
    image_path: str
    masks: list = field(default_factory=list)
    filterd_mask: list = field(default_factory=list)
    path_node: list = field(default_factory=list)
    size_of_path: int = 0
    valid_mask_id: list = field(default_factory=list)
    distance_matrix: np.matrix = field(default_factory=lambda: np.matrix([]))
    image: list = field(default_factory=list)
    
    row_counting_left_start = None 
    row_counting_right_start = None
    
    path_nodes_right : list = field(default_factory=list)
    path_nodes_left : list = field(default_factory=list)

    @property
    def mask_size(self):
        return len(self.masks)

    @property
    def mask_valid_size(self):
        return len(self.valid_mask_id)
    
    def save_to_file(self, filename: str):
        """Save the object to pickle file"""
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_from_file(filename: str):
        """Load the object from a file using pickle."""
        with open(filename, 'rb') as f:
            return pickle.load(f)
        
    def __str__(self) -> str:
        return f"Image path: {self.image_path}"

if __name__  == "__main__":
    # Test the class corn_data
    print("Testing the CornData class")
    corn_data = CornData("path_to_image.jpg")
    print(corn_data)
