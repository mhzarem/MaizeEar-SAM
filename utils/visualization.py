import cv2
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Models.corn_data import CornData

os.environ["KMP_DUPLICATE_LIB_OK"] = "True"


class Visual:
    def __init__(self, image):
        self.image = image

    def show_hsv(self):
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        H, S, V = cv2.split(hsv)
        self._show_image([H, S, V, hsv], ["H", "S", "V", "HSV"])

    def show_rgb(self):
        rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        R, G, B = cv2.split(rgb)
        self._show_image([R, G, B, rgb], ["R", "G", "B", "RGB"], ['Reds', 'Greens', 'Blues'])

    def show_lab(self):
        lab = cv2.cvtColor(self.image, cv2.COLOR_BGR2LAB)
        L, A, B = cv2.split(lab)
        self._show_image([L, A, B, lab], ["L", "A", "B", "LAB"])

    def show_luv(self):
        luv = cv2.cvtColor(self.image, cv2.COLOR_BGR2LUV)
        L, U, V = cv2.split(luv)
        self._show_image([U, L, V, luv], ["L", "U", "V", "LUV"])


    @staticmethod
    def show_path(corndata: CornData, path_nodes):
        plt.figure(figsize=(4,12))
        plt.imshow(corndata.image)
        color = 'g'  # green
        thickness = 4
        # plt.axis('off')
        # Draw lines between consecutive points
        for i in range(len(path_nodes) - 1):
            start_point = (int(corndata.filterd_mask[path_nodes[i]]['centroid'][0]), int(corndata.filterd_mask[path_nodes[i]]['centroid'][1]))
            end_point = (int(corndata.filterd_mask[path_nodes[i+1]]['centroid'][0]), int(corndata.filterd_mask[path_nodes[i+1]]['centroid'][1]))
            plt.plot([start_point[0], end_point[0]], [start_point[1], end_point[1]], color=color, linewidth=thickness)
            x,y = corndata.filterd_mask[path_nodes[i]]['centroid']
            plt.scatter(x,y , c='r')   
        plt.show()
        plt.close()
    

    @staticmethod
    def _show_image(images: list, titles: list, cmaps: list = ['gist_yarg', 'gist_yarg', 'gist_yarg']):
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(20, 15))

        fig.suptitle(f"This image show {titles[3]}", fontsize=25)

        # Display the first image
        ax1.imshow(images[0], cmap=cmaps[0])
        ax1.set_title(titles[0])
        ax1.axis("off")

        # Display the second image
        ax2.imshow(images[1], cmap=cmaps[1])
        ax2.set_title(titles[1])
        ax2.axis("off")

        # Display the third image
        ax3.imshow(images[2], cmap=cmaps[2])
        ax3.set_title(titles[2])
        ax3.axis("off")

        # Display the first image
        ax4.imshow(images[3])
        ax4.set_title(titles[3])
        ax4.axis("off")

        # Show the plot
        plt.show()

def show_path_on_corn(corndata: CornData):
    plt.figure(figsize=(4,12))
    plt.imshow(corndata.image)
    color = 'g'  # green
    thickness = 4
    plt.axis('off')
    # Draw lines between consecutive points
    for i in range(len(corndata.path_node) - 1):
        start_point = (int(corndata.filterd_mask[corndata.path_node[i]]['centroid'][0]), int(corndata.filterd_mask[corndata.path_node[i]]['centroid'][1]))
        end_point = (int(corndata.filterd_mask[corndata.path_node[i+1]]['centroid'][0]), int(corndata.filterd_mask[corndata.path_node[i+1]]['centroid'][1]))
        plt.plot([start_point[0], end_point[0]], [start_point[1], end_point[1]], color=color, linewidth=thickness)
        x,y = corndata.filterd_mask[corndata.path_node[i]]['centroid']
        plt.scatter(x,y , c='r')   
    plt.show()
    plt.close()