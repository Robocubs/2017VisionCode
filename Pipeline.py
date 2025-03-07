import cv2
import numpy
import math
from enum import Enum
class GripPipeline:
    """
    A merged OpenCV pipeline created by GRIP.
    """
    def __init__(self, blue):
        """
        Initialize all values to presets or None they need to be set.
        """
        if blue == True:
            self.__rgb_threshold_red = [0.0, 29.872665534804735]
            self.__rgb_threshold_green = [0.0, 255.0]
            self.__rgb_threshold_blue = [89.43345323741006, 255.0]
        else:
            self.__rgb_threshold_red = [94.01978417266189, 200.88285229202037]
            self.__rgb_threshold_green = [41.276978417266186, 144.60101867572158]
            self.__rgb_threshold_blue = [41.276978417266186, 131.61290322580643]
        self.rgb_threshold_output = None
        self.__find_contours_input = self.rgb_threshold_output
        self.__find_contours_external_only = False
        self.find_contours_output = None
        self.__filter_contours_contours = self.find_contours_output
        if blue == True:
            self.__filter_contours_min_area = 20.0
            self.__filter_contours_min_perimeter = 0
            self.__filter_contours_min_width = 23.0
            self.__filter_contours_max_width = 1000
            self.__filter_contours_min_height = 0.0
            self.__filter_contours_max_height = 1000.0
            self.__filter_contours_solidity = [0, 100]
            self.__filter_contours_max_vertices = 1000000
            self.__filter_contours_min_vertices = 0
            self.__filter_contours_min_ratio = 0
            self.__filter_contours_max_ratio = 1000
        else:
            self.__filter_contours_min_area = 40.0
            self.__filter_contours_min_perimeter = 80.0
            self.__filter_contours_min_width = 0.0
            self.__filter_contours_max_width = 200.0
            self.__filter_contours_min_height = 40.0
            self.__filter_contours_max_height = 1000.0
            self.__filter_contours_solidity = [0, 100]
            self.__filter_contours_max_vertices = 140.0
            self.__filter_contours_min_vertices = 10.0
            self.__filter_contours_min_ratio = 0.0
            self.__filter_contours_max_ratio = 1000.0
        self.filter_contours_output = None
    def process(self, source0):
        """
        Run the pipeline and set all outputs to new values.
        """
        # Step RGB_Threshold0:
        self.__rgb_threshold_input = source0
        (self.rgb_threshold_output) = self.__rgb_threshold(self.__rgb_threshold_input, self.__rgb_threshold_red, self.__rgb_threshold_green, self.__rgb_threshold_blue)
        # Step Find_Contours0:
        self.__find_contours_input = self.rgb_threshold_output
        (self.find_contours_output) = self.__find_contours(self.__find_contours_input, self.__find_contours_external_only)
        # Step Filter_Contours0:
        self.__filter_contours_contours = self.find_contours_output
        (self.filter_contours_output) = self.__filter_contours(self.__filter_contours_contours, self.__filter_contours_min_area, self.__filter_contours_min_perimeter, self.__filter_contours_min_width, self.__filter_contours_max_width, self.__filter_contours_min_height, self.__filter_contours_max_height, self.__filter_contours_solidity, self.__filter_contours_max_vertices, self.__filter_contours_min_vertices, self.__filter_contours_min_ratio, self.__filter_contours_max_ratio)
    
    @staticmethod
    def __rgb_threshold(input, red, green, blue):
        """Segment an image based on color ranges.
        Args:
            input: A BGR numpy.ndarray.
            red: A list of two numbers the are the min and max red.
            green: A list of two numbers the are the min and max green.
            blue: A list of two numbers the are the min and max blue.
        Returns:
            A black and white numpy.ndarray.
        """
        out = cv2.cvtColor(input, cv2.COLOR_BGR2RGB)
        return cv2.inRange(out, (red[0], green[0], blue[0]),  (red[1], green[1], blue[1]))

    @staticmethod
    def __find_contours(input, external_only):
        """
        Sets the values of pixels in a binary image to their distance to the nearest black pixel.
            input: A numpy.ndarray.
            external_only: A boolean. If true only external contours are found.
        Returns a list of numpy.ndarray values where each one represents a contour.
        """
        if(external_only):
            mode = cv2.RETR_EXTERNAL
        else:
            mode = cv2.RETR_LIST
        method = cv2.CHAIN_APPROX_SIMPLE
        im2, contours, hierarchy =cv2.findContours(input, mode=mode, method=method)
        return contours

    @staticmethod
    def __filter_contours(input_contours, min_area, min_perimeter, min_width, max_width,
                        min_height, max_height, solidity, max_vertex_count, min_vertex_count,
                        min_ratio, max_ratio):
        """Filters out contours that do not meet certain criteria.
        Args:
            input_contours: Contours as a list of numpy.ndarray.
            min_area: The minimum area of a contour that will be kept.
            min_perimeter: The minimum perimeter of a contour that will be kept.
            min_width: Minimum width of a contour.
            max_width: MaxWidth maximum width.
            min_height: Minimum height.
            max_height: Maximimum height.
            solidity: The minimum and maximum solidity of a contour.
            min_vertex_count: Minimum vertex Count of the contours.
            max_vertex_count: Maximum vertex Count.
            min_ratio: Minimum ratio of width to height.
            max_ratio: Maximum ratio of width to height.
        Returns:
            Contours as a list of numpy.ndarray.
        """
        output = []
        for contour in input_contours:
            x,y,w,h = cv2.boundingRect(contour)
            if (w < min_width or w > max_width):
                continue
            if (h < min_height or h > max_height):
                continue
            area = cv2.contourArea(contour)
            if (area < min_area):
                continue
            if (cv2.arcLength(contour, True) < min_perimeter):
                continue
            hull = cv2.convexHull(contour)
            solid = 100 * area / cv2.contourArea(hull)
            if (solid < solidity[0] or solid > solidity[1]):
                continue
            if (len(contour) < min_vertex_count or len(contour) > max_vertex_count):
                continue
            ratio = (float)(w) / h
            if (ratio < min_ratio or ratio > max_ratio):
                continue
            output.append(contour)
        return output
