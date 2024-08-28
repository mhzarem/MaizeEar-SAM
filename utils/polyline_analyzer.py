import matplotlib.pyplot as plt

class PolylineAnalyzer:
    def __init__(self, polyline):
        self.polyline = polyline
        
    def intersection_point(self, p, p1, p2):
        """Find the intersection point of the horizontal line from point p with the segment p1-p2."""
        if p1[1] == p2[1]:  # If the segment is horizontal
            return None

        # If the point's y-coordinate is between the y-coordinates of the segment endpoints
        if min(p1[1], p2[1]) <= p[1] <= max(p1[1], p2[1]):
            x_intersection = p1[0] + (p[1] - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])
            return (x_intersection, p[1])
        return None
    
    def position_relative_to_polyline(self, point):
        """Determine if the point is to the left or right of the polyline."""
        for p1, p2 in zip(self.polyline[:-1], self.polyline[1:]):
            intersect_pt = self.intersection_point(point, p1, p2)
            if intersect_pt:
                if point[0] > intersect_pt[0]:
                    return "right"
                elif point[0] < intersect_pt[0]:
                    return "left"
        return None

    @staticmethod
    def add_guard_points(polyline, y_bounds=(0, 12)):
        """Add guard points to the given polyline."""
        # Find the x value of the polyline point with the lowest y value
        min_y_point = min(polyline, key=lambda p: p[1])
        # Find the x value of the polyline point with the highest y value
        max_y_point = max(polyline, key=lambda p: p[1])
        
        # Add a point at the bottom boundary with the x-value of min_y_point
        # and another point at the top boundary with the x-value of max_y_point
        augmented_polyline = [(min_y_point[0], y_bounds[0])] + polyline + [(max_y_point[0], y_bounds[1])]
        
        return augmented_polyline
        
    def categorize_points(self, test_points):
        """Categorize points as either left or right of the polyline."""
        right_points = []
        left_points = []
        
        for idx, point in enumerate(test_points):
            position = self.position_relative_to_polyline(point)
            if position == "right":
                right_points.append(idx)
            elif position == "left":
                left_points.append(idx)
        
        return right_points, left_points
   
    def visualize(self, test_points, image):
        plt.figure(figsize=(4,12))
        plt.imshow(image)
        # _image_height, _image_width = image.shape[:2]
        # plt.xlim([0, _image_width])
        # plt.ylim([_image_height, 0])

        # Plot the polyline
        x_coords, y_coords = zip(*self.polyline)
        plt.plot(x_coords, y_coords, color='black', marker='o', label='Polyline')

        # Plot the test points based on their position
        for point in test_points:
            position = self.position_relative_to_polyline(point)
            if position == "right":
                plt.scatter(point[0], point[1], color='red', s=10)
            elif position == "left":
                plt.scatter(point[0], point[1], color='blue', s=10)
            else:
                plt.scatter(point[0], point[1], color='green', s=10)

        plt.title('Position of Points relative to the Polyline')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid(True)
        plt.show()