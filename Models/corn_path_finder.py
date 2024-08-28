import math 
import numpy as np
import networkx as nx
import sys
sys.path.append("../utils")
from polyline_analyzer import PolylineAnalyzer

from corn_data import CornData

class CornPathFinder:

    def __init__(self, corndata: CornData):
        self.corndata = corndata
        self.start_point_id: int 
        self.stop_point_id: int
        self.adj_matrix: np.matrix

    def find_distance_matrix(self):
        """
        this function calculate the distance between two centroid of the kernels
        """

        self.corndata.distance_matrix = np.zeros((self.corndata.mask_valid_size, self.corndata.mask_valid_size, 3), dtype=float)
        
        for index_i, element_i in enumerate(self.corndata.valid_mask_id):
            for index_j, element_j in enumerate(self.corndata.valid_mask_id):
                
                cX_i, cY_i = self.corndata.masks[element_i]['centroid']
                cX_j, cY_j = self.corndata.masks[element_j]['centroid']
                
                dist = math.sqrt((cX_i - cX_j) ** 2 + (cY_i - cY_j) ** 2)
                dist_x = abs(cX_i - cX_j)
                dist_y = abs(cY_i - cY_j)
                
                self.corndata.distance_matrix[index_i][index_j][:] = [dist, dist_x, dist_y]


    def find_start_point(self):
        """
        find the start point id for construct the path
        """
        centroids = np.array([d['centroid'] for d in self.corndata.filterd_mask])
        sorted_indices = np.argsort(centroids[:,1], axis=None)
        self.start_point_id = sorted_indices[1]  # second smallest
        
    def find_stop_point(self):
        """
        find the stop point id  for construct the path
        """
        centroids = np.array([d['centroid'] for d in self.corndata.filterd_mask])
        sorted_indices = np.argsort(centroids[:,1], axis=None)
        self.stop_point_id = sorted_indices[-2]  # second largest
    
    @staticmethod
    def distance(point1, point2):
        return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
    @staticmethod
    def angle_between(point1, point2, center):
        vector1 = [point1[0] - center[0], point1[1] - center[1]]
        vector2 = [point2[0] - center[0], point2[1] - center[1]]
        dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
        magnitude1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
        magnitude2 = math.sqrt(vector2[0]**2 + vector2[1]**2)
        cos_angle = np.clip(dot_product / (magnitude1 * magnitude2), -1.0, 1.0)
        angle = math.degrees(math.acos(cos_angle))
        return angle
        
    def construct_adjancy_matrix(self):
        
         # try to calculate the good threshould 
        data = self.corndata.distance_matrix
        # make the adjency matrix based on the n nearest neibghbors    
        adj_matrix = np.zeros((self.corndata.mask_valid_size, self.corndata.mask_valid_size), dtype=int)

        for i, row in enumerate(data):
            # Sort by distance but keep track of original indices
            sorted_indices = np.argsort(row[:, 0])

            # Get the first 4 nearest neighbors' indices (excluding itself)
            four_nearest_neighbors = sorted_indices[1:4]
            filtered_neighbors = []

            # Populate adjacency matrix
            for j in four_nearest_neighbors:
                center = self.corndata.filterd_mask[i]['centroid']
                point1 = self.corndata.filterd_mask[j]['centroid']
                
                keep = True
                for k in four_nearest_neighbors:
                     if k != j:
                         point2 = self.corndata.filterd_mask[k]['centroid']
                         angle = CornPathFinder.angle_between(point1, point2, center)
    
                         if angle < 20:  # You can adjust this angle
                            # Remove the farther point
                            if CornPathFinder.distance(center, point1) > CornPathFinder.distance(center, point2):
                                keep = False
                                break
                if keep:
                    filtered_neighbors.append(j)
                    
    
            for j in filtered_neighbors:  
                adj_matrix[i, j] = adj_matrix[j, i] = row[j, 0]

            self.adj_matrix = adj_matrix

    #todo: agregate this two adjacny matrix
    
    @staticmethod
    def st_construct_adjacency_matrix(corndata, subset=None):
        # If subset is not provided, use the entire dataset
        if subset is None:
            subset = range(corndata.mask_valid_size)
        
        # Try to calculate a good threshold
        data = corndata.distance_matrix
        # Create an adjacency matrix based on the n nearest neighbors
        adj_matrix = np.zeros((len(subset), len(subset)), dtype=int)
    
        for idx, i in enumerate(subset):
            row = data[i]
            # Sort by distance but keep track of original indices
            sorted_indices = np.argsort(row[:, 0])
            
            # Filter the sorted indices to only include those in our subset
            sorted_indices = [index for index in sorted_indices if index in subset]
    
            # Get the first 4 nearest neighbors' indices (excluding itself)
            num_neighbors = 7
            four_nearest_neighbors = sorted_indices[1:num_neighbors]
            filtered_neighbors = []
    
            # Populate adjacency matrix
            for j in four_nearest_neighbors:
                center = corndata.filterd_mask[i]['centroid']
                point1 = corndata.filterd_mask[j]['centroid']
                
                keep = True
                for k in four_nearest_neighbors:
                     if k != j:
                         point2 = corndata.filterd_mask[k]['centroid']
                         angle = CornPathFinder.angle_between(point1, point2, center)
    
                         if angle < 20:  # You can adjust this angle
                            # Remove the farther point
                            if CornPathFinder.distance(center, point1) > CornPathFinder.distance(center, point2):
                                keep = False
                                break
                if keep:
                    filtered_neighbors.append(j)
                    
            for j in filtered_neighbors:
                adj_matrix[idx, subset.index(j)] = adj_matrix[subset.index(j), idx] = row[j,0]
    
        return adj_matrix
      
    def find_path(self):
        # make the path
        try:
            G = nx.from_numpy_array(self.adj_matrix)
            path = nx.dijkstra_path(G,self.start_point_id,self.stop_point_id)
            self.corndata.path_node = path
            # print(f"the central path length is {len(path)}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    

    @staticmethod
    def st_find_path(adj_matrix, start_point_id, stop_point_id):
        

        try: 
        # Create a graph from the adjacency matrix
            G = nx.from_numpy_array(adj_matrix)
            
            # Find the shortest path using Dijkstra's algorithm
            path = nx.dijkstra_path(G, start_point_id, stop_point_id)
            
            return path
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

####  this code finds the prepheral path
####  THIS CODE SHOULD BE REFACTORED
    @staticmethod
    def find_start_point_prepheral(data, sublist):
        """
        Find the start point id for constructing the path.
        Returns both the original ID and its index within the sublist.
        """
        centroids = [(data.filterd_mask[i]['centroid'][1], i) for i in sublist]
        sorted_centroid_listed = sorted(centroids, key=lambda x: x[0])
        
        original_id = sorted_centroid_listed[1][1]
        sublist_index = sublist.index(original_id)
        
        return original_id, sublist_index
    @staticmethod
    def find_stop_point_prepheral(data, sublist):
        """
        Find the start point id for constructing the path.
        Returns both the original ID and its index within the sublist.
        """
        centroids = [(data.filterd_mask[i]['centroid'][1], i) for i in sublist]
        sorted_centroid_listed = sorted(centroids, key=lambda x: x[0],reverse=True)
        
        original_id = sorted_centroid_listed[1][1]
        sublist_index = sublist.index(original_id)
        
        return original_id, sublist_index

    def find_pripheral_paths(self):
            
        try:
            center_path_nodes = [self.corndata.filterd_mask[item]['centroid'] for item in self.corndata.path_node]

            all_nodes_center = [item['centroid'] for item in self.corndata.filterd_mask]

            _image_height, _image_width = self.corndata.image.shape[:2]

            # adding the two point in the top part and bottom part of the image to divide the image totally into two part
            polyline_points = PolylineAnalyzer.add_guard_points(center_path_nodes,(0,_image_height))

            analyzer = PolylineAnalyzer(polyline_points)

            test_points = all_nodes_center
            
            right_id , left_id = analyzer.categorize_points(test_points)



            original_id_start_right, sublist_index_start_right = self.find_start_point_prepheral(self.corndata, right_id)
            original_id_stop_right, sublist_index_stop_right = self.find_stop_point_prepheral(self.corndata, right_id)


            adj_matrix_right = CornPathFinder.st_construct_adjacency_matrix(self.corndata,right_id)

            # Running the find_path method
            path_result_right = self.st_find_path(adj_matrix_right, sublist_index_start_right, sublist_index_stop_right)

            #print the size of that path
            # print(f"the right path length is {len(path_result_right)}")

            original_id_start_left, sublist_index_start_left = self.find_start_point_prepheral(self.corndata, left_id)
            original_id_stop_left, sublist_index_stop_left = self.find_stop_point_prepheral(self.corndata, left_id)
            adj_matrix_left = CornPathFinder.st_construct_adjacency_matrix(self.corndata,left_id)
            path_result_left = self.st_find_path(adj_matrix_left, sublist_index_start_left, sublist_index_stop_left)
            # print(f"the left path lenght is {len(path_result_left)}")     
            


            self.corndata. path_nodes_right = path_result_right
            self.corndata. path_nodes_left = path_result_left        

            return path_result_right, path_result_left

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None, None
#### end of the code that find the prepheral path
#### this code should be refactored

    def make_path(self):
        self.find_distance_matrix()
        self.find_start_point()
        self.find_stop_point()
        self.construct_adjancy_matrix()
        self.find_path()
        self.find_pripheral_paths()