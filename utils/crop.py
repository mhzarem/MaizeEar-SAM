import cv2
import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

class Crop:
    
    """
    This class is used to crop the indivisual maize ear from the raw image.

    EXAMPLE USEAGE:

    raw_image_path = "/work/mech-ai-scratch/zare/Edge/Data/crop_test_image/Raw/22-A-1550275.png"
    croped_images_folder = "/work/mech-ai-scratch/zare/Edge/Data/crop_test_image/Croped"
    crop = Crop(raw_image_path, croped_images_folder)
    crop.crop_image()

    """

    def __init__(self, raw_image_path, croped_images_folder):
            """
            Initializes a Crop object.

            Args:
                raw_image_path (str): The path to the raw image.
                croped_images_folder (str): The folder where the cropped images will be saved.
            """
            
            self.raw_image_path = raw_image_path
            self.croped_images_folder = croped_images_folder

    def read_image(self):
        img = cv2.imread(self.raw_image_path)
        if img is None:
            raise FileNotFoundError(f"The file '{self.read_path}' does not exist.")
        else:
            return img

    def save_image(self, sorted_list: list):

        raw_image_file_name = os.path.basename(self.raw_image_path)
        raw_image_file_name_wt_extension =  Path(raw_image_file_name).stem

        if os.path.exists(self.croped_images_folder):
            directory = os.path.join(self.croped_images_folder,raw_image_file_name_wt_extension)
            
            # Check if the number of maize ear is 4 in the image 
            # we knew that the number of maize ear is 4 on the image
            # if the number of maize ear is not 4 then we will not save the image
            
            if len(sorted_list) == 4:       
                os.makedirs(directory, exist_ok=True)
                for index, data  in enumerate(sorted_list):
                    croped_ear_file_name = raw_image_file_name_wt_extension + "-" + str(index + 21) + " OP.png"
                    write_path = os.path.join(directory , croped_ear_file_name)
                    cv2.imwrite(write_path, data[0])
                print(f"The {len(sorted_list)} maize ear is saved in {directory}")
            else:
                print(f"Number of maize ear is not 4 in {raw_image_file_name}")
    
    
    def has_significant_yellow(self,image, threshold_percentage=7.0):
        """
        Check if an image has yellow content above a specified threshold percentage.

        Returns:
        - bool: True if yellow content is above the threshold, False otherwise.
        """
        
        # Convert the image from BGR to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Define range for yellow color in HSV
        lower_yellow = np.array([20, 130, 100])
        upper_yellow = np.array([40, 255, 255])
        
        # Create a binary mask where yellow regions are white and the rest are black
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        
        # Calculate the percentage of pixels that are yellow
        yellow_percentage = (np.sum(mask > 0) / mask.size) * 100
        
        return yellow_percentage > threshold_percentage

    def crop_image(self):
        
        image = self.read_image()
        # Convert the image to grayscale for thresholding
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        H, S, V = cv2.split(hsv)
        # Apply threshold
        _, thresholded_image = cv2.threshold(V, 127, 255, cv2.THRESH_BINARY)
        # Find contours
        contours, _ = cv2.findContours(thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        y_rois = []
        for contour in contours:
            # Get bounding box
            x, y, w, h = cv2.boundingRect(contour)
            roi = image[y:y+h, x:x+w]  
            # Restrictions on contour size (area) and average color
            if cv2.contourArea(contour) > 100000:
                # check if the image has significant yellow color
                if self.has_significant_yellow(roi,0.9):
                    y_rois.append([image[y:y+h, x:x+w],x])
            # save the images and also the bonding box around the cobs 
        sorted_list = sorted(y_rois, key=lambda x: x[1], reverse=True)
        self.save_image(sorted_list) 


if __name__ == "__main__":

    raw_image_path = "/work/mech-ai-scratch/zare/Edge/Data/crop_test_image/Raw/22-A-1550275.png"
    croped_images_folder = "/work/mech-ai-scratch/zare/Edge/Data/crop_test_image/Croped"
    crop = Crop(raw_image_path, croped_images_folder)
    crop.crop_image()