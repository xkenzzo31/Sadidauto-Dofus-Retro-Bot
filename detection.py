from typing import Tuple, Any
import cv2 as cv
import numpy as np
from paddleocr import PaddleOCR


class Detection:


    # Constants.
    # The region of the screen where screenshots for 'haystack' images 
    # are made. This value should NEVER be touched. The width and height
    # values aren't the same as the 'Dofus.exe' window itself, because 
    # 'pyautogui.screenshot()' captures a little more than needed.
    GAMEWINDOW_DEFAULT_REGION = (0, 0, 933, 755)

    # Attributes.
    opencv_match_method = None
    needle_img = None
    needle_w = 0
    needle_h = 0
    
    # Constructor.
    def __init__(self, 
                 opencv_match_method: int | None = cv.TM_CCOEFF_NORMED):

        # Loading the default match method that 'cv_matchTemplate' will
        # be using.
        self.opencv_match_method = opencv_match_method

    def find(self, 
             haystack_img: np.ndarray, 
             needle_img: np.ndarray, 
             threshold: float | None = 0.9) -> tuple | list[list[int]]:
        """Find 'needle' image on 'haystack' image.

        Parameters
        ----------
        haystack_img : np.ndarray or str
            Image to search on. Can be `np.ndarray` or `str` path to 
            the image.
        needle_img : np.ndarray or str
            Image to search for. Can be `np.ndarray` or `str` path to 
            the image.
        threshold : float, optional
            Accuracy with which `needle_img` will be searched for 
            (0.0 to 1.0). Defaults to 0.9. 

        Returns
        ----------
        rectangles : tuple
            Empty `tuple` if no matches found.
        rectangles : list[list[int]]
            2D `list` containing bounding box information of found 
            matches. Example: [[topLeft_x, topLeft_y, width, height]].

        Raises
        ---------
        Overload resolution failed
            If `haystack_img` or `needle_img` are not `np.ndarray` or 
            `str`.
        (-215:Assertion failed) in function 'cv::matchTemplate'
            If `haystack_img` or `needle_img` do not exist in the 
            specified `str` path.
        (-215:Assertion failed) in function 'cv::matchTemplate'
            If `haystack_img` and `needle_img` are read into memory
            differently.
            Example: `haystack_img` is 'BGR' and `needle_img` is 'GRAY'.
        """
        # If 'haystack_img' or/and 'needle_img' are passed in as 'str'
        # paths to images, convert them to 'numpy.ndarray' by reading 
        # into memory.
        if isinstance(haystack_img, str):
            haystack_img = cv.imread(haystack_img, cv.IMREAD_UNCHANGED)
        if isinstance(needle_img, str):
            needle_img = cv.imread(needle_img, cv.IMREAD_UNCHANGED)

        # Using matchTemplate to find 'needle_img' in 'haystack_img'.
        result = cv.matchTemplate(haystack_img, 
                                  needle_img, 
                                  self.opencv_match_method)

        # Finding best matches (using threshold) and getting the (x, y) 
        # coordinates of top left corners of those matches.
        locations: Any = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        # Creating a list of rectangles that stores bounding box 
        # information of found matches (topLeft_x, topLeft_y, w, h).
        # The list is later used in 'cv.groupRectangles()'.
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), 
                    int(loc[1]), 
                    needle_img.shape[1], 
                    needle_img.shape[0]]

            # Appending to the list twice because 'cv.groupRectangles()' 
            # requires at least two overlapping rectangles for it group
            # them together. If only appending once, 
            # 'cv.groupRectangles()' will throw out any results 
            # (even if they're correct) that do not overlap.
            rectangles.append(rect)
            rectangles.append(rect)

        # Grouping all rectangles that are close by.
        rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)
        
        return rectangles

    def get_click_coords(self, 
                         rectangles: list[list[int]]) -> list[Tuple[int, int]]:
        """Calculate center (x, y) coordinates of bounding box.

        Parameters
        ----------
        rectangles : list[list[int]]
            2D `list` containing [[topLeft_x, topLeft_y, width, height]]
            of bounding box.

        Returns
        ----------
        coords : list[Tuple[int, int]]
            `list` of tuples containing (x, y) coordinates.
        """
        coords = []

        for (x, y, w, h) in rectangles:
            
            # Determining the center positions of found matches.
            center_x = x + int(w/2)
            center_y = y + int(h/2)

            # Saving the center positions.
            coords.append((center_x, center_y))

        return coords

    # Draws a box around found objects using (x, y, w, h) coordinates 
    # provided by 'find()' method.
    # 'rectangles' must be a list of lists, or list of tuples.
    def draw_rectangles(self, 
                        haystack_img, 
                        rectangles, 
                        line_color=(0, 255, 0), 
                        line_thickness=2):

        line_color = line_color
        line_thickness = line_thickness

        for (x, y, w, h) in rectangles:

            # Determine the box positions.
            top_left = (x, y)
            bottom_right = (x + w, y + h)

            # Draw the box/rectangle.
            cv.rectangle(haystack_img, 
                         top_left, 
                         bottom_right, 
                         line_color, 
                         line_thickness)

        return haystack_img

    # Draws markers on center (x, y) coordinates of found objects. 
    # 'points' can be generated by 'get_click_coords()' method.
    def draw_crosshairs(self, haystack_img, points):

        marker_color = (255, 0, 255)
        marker_type = (cv.MARKER_CROSS)

        for (center_x, center_y) in points:

            # Drawing markers on the center positions of found matches.
            cv.drawMarker(haystack_img, 
                         (center_x, center_y), 
                          marker_color, 
                          marker_type)

        return haystack_img

    # Detects provided 'objects_to_detect_list' (string names of images) 
    # on a 'haystack_image'. Doesn't work when there's only 1 'image' 
    # in the 'objects_to_detect_list'. Must be at least 2. Can be the 
    # same image string copied twice. Doesn't work very well though. 
    # This method is best used when trying to detect multiple (>10) 
    # objects. Like detecting monsters for example. If accurate results 
    # for 1 object is required, then it's best to use 'find()'.
    def detect_objects(self, 
                       objects_to_detect_list, 
                       objects_to_detect_path, 
                       haystack_image, 
                       threshold=0.6):

        # Looping over all needle images and trying to find them on the 
        # haystack image (screenshot). Appending all information of 
        # found matches to an empty list. This generates a list of 2D 
        # numpy arrays.
        object_rectangles = []
        for image in objects_to_detect_list:

            rectangles = self.find(haystack_image, 
                                   objects_to_detect_path + image, 
                                   threshold)
            object_rectangles.append(rectangles)

        # Converting a list of 2D numpy arrays into a list of 1D numpy 
        # arrays.
        object_rectangles_converted = []
        for i in object_rectangles:
            for j in i:
                object_rectangles_converted.append(j)

        # Converting a list of 1D numpy arrays into one 2D numpy array.
        object_rectangles_converted = np.array(object_rectangles_converted)

        # Grouping all rectangles that are close-by to reduce amount of 
        # matches.
        object_rectangles_converted, weights = cv.groupRectangles(
                                                object_rectangles_converted, 
                                                1, 
                                                0.5)

        # Creating a list containing center (x, y) coordinates of found
        # matches.
        object_center_xy_coordinates = self.get_click_coords(
                                                   object_rectangles_converted)

        return object_rectangles_converted, object_center_xy_coordinates

    # Detects text on a provided image. The 'image_path' must be a 
    # string or 'np.ndarray'.
    def ocr_detect_text_from_image(self, 
                                   image_path, 
                                   lang="en", 
                                   use_angle_cls=True, 
                                   gpu=False, 
                                   show_log=False):

        if isinstance(image_path, str):
            image_path = cv.imread(image_path, cv.IMREAD_UNCHANGED)

        ocr = PaddleOCR(lang=lang, 
                        use_angle_cls=use_angle_cls, 
                        gpu=gpu, 
                        show_log=show_log)

        results = ocr.ocr(image_path)
    
        # results[0][0][0] are [x, y] coordinates of the TOP LEFT 
        # corner of the bounding box.
        # results[0][0][2] are [x, y] coordinates of the BOTOOM RIGHT 
        # corner of the bounding box.
        # results[0][1][0] is the text found within the bounding box.
        # results[0][1][1] is the confidence parameter.

        # Getting bounding box information of detected results.
        boxes = [result[0] for result in results]

        # Getting (x, y, w, h) of the bounding boxes. This format is
        #  needed for 'draw_rectangles()' method.
        rectangles = [(int(box[0][0]), 
                       int(box[0][1]), 
                       int(box[2][0]) - int(box[0][0]), 
                       int(box[2][1]) - int(box[0][1])) 
                       for box in boxes]
                       
        # Getting all detected text.
        text = [result[1][0] for result in results]

        # Creating a list which stores (x, y, w, h) of the bounding box, 
        # and text found within that bounding box.
        rectangles_and_text = []
        for i in range(len(rectangles)):
            rectangles_and_text.append([[rectangles[i]], text[i]])

        return rectangles_and_text, rectangles, text
