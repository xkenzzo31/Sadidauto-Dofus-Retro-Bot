import cv2 as cv
import numpy as np
import pyautogui
import threading


class Detection:

    # Threading Properties
    stopped = True
    lock = None
    screenshot = None

    # Properties
    GAMEWINDOW_DEFAULT_REGION = (0, 30, 935, 725)
    GAMEWINDOW_OFFSET_X = GAMEWINDOW_DEFAULT_REGION[0]
    GAMEWINDOW_OFFSET_Y = GAMEWINDOW_DEFAULT_REGION[1]

    needle_img = None
    needle_w = 0
    needle_h = 0
    method = None

    # Constructor
    def __init__(self, needle_img_path, method=cv.TM_CCOEFF_NORMED):

        # Creating a thread lock object
        self.lock = threading.Lock()

        # Only load these variables if a specific needle_img is passed in
        if needle_img_path:
            # Loading the needle_image
            self.needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)
            # Saving dimensions of needle_image
            self.needle_w = self.needle_img.shape[1]
            self.needle_h = self.needle_img.shape[0]

        # Loading the match method that cv_matchTemplate will be using (there are several to choose from in OpenCV docs)
        # Default method will be: cv.TM_CCOEFF_NORMED
        self.method = method


    def find(self, haystack_img, threshold=0.6):

        # Using matchTemplate to find needle_img in haystack_img
        result = cv.matchTemplate(haystack_img, self.needle_img, self.method)

        # Finding best matches (using threshold) and getting the (x, y) coordinates of those matches
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        # Creating a list of rectangles that stores information of the found matches (x, y, w, h)
        # The list is later used in groupRectangles() function
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_w, self.needle_h]
            rectangles.append(rect)
            rectangles.append(rect)

        # Grouping all rectangles that are close by
        rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)

        return rectangles


    def get_click_points(self, rectangles):

        points = []
        for (x, y, w, h) in rectangles:
            
            # Determining the center positions of found matches
            center_x = x + int(w/2)
            center_y = y + int(h/2)
            # Saving the center positions
            points.append((center_x, center_y))

        return points


    # These offset coordinates are used when script needs to click on found needle_imgs with pyautogui or other.
    # It converts the (x, y) coordinates found on the haystack_img to clickable coordinates on screen.
    def get_offset_click_points(self, coordinates):
        return (coordinates[0] + self.GAMEWINDOW_OFFSET_X, coordinates[1] + self.GAMEWINDOW_OFFSET_Y)

        
    def draw_rectangles(self, haystack_img, rectangles):

        line_color = (0, 255, 0)
        line_type = cv.LINE_4

        for (x, y, w, h) in rectangles:
            # Determining the box positions
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            # Draw the box/rectangle
            cv.rectangle(haystack_img, top_left, bottom_right, line_color, line_type)

        return haystack_img


    def draw_crosshairs(self, haystack_img, points):

        marker_color = (255, 0, 255)
        marker_type = (cv.MARKER_CROSS)

        for (center_x, center_y) in points:
            # Drawing markers on the center positions of found matches
            cv.drawMarker(haystack_img, (center_x, center_y), marker_color, marker_type)

        return haystack_img

    
    # Screenshoting specified region of the screen. The default is whole game window. 
    # Converting screenshot into required format and returning it.
    def gamewindow_capture(self, capture_region=GAMEWINDOW_DEFAULT_REGION):

        screenshot = pyautogui.screenshot(region=capture_region) # Region set for (950, 765) size Dofus Window (w, h)
        screenshot = np.array(screenshot)
        screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)

        return screenshot


    def detect_object(self, images_list, images_folder_path, threshold=0.6, capture_region_coordinates=GAMEWINDOW_DEFAULT_REGION):

        # Getting an updated screenshot (haystack) of the game
        screenshot = self.gamewindow_capture(capture_region=capture_region_coordinates)

        # Looping over all needle images and appending all information of found matches to an empty list
        # This generates a list of 2D numpy arrays
        object_rectangles = []
        for image in images_list:
            detection = Detection(images_folder_path + image)
            rectangles = detection.find(screenshot, threshold)
            object_rectangles.append(rectangles)

        # Converting a list of 2D numpy arrays into a list of 1D numpy arrays
        object_rectangles_converted = []
        for i in object_rectangles:
            for j in i:
                object_rectangles_converted.append(j)

        # Converting a list of 1D numpy arrays into one 2D numpy array
        object_rectangles_converted = np.array(object_rectangles_converted)

        # Grouping all rectangles that are close-by to reduce amount of matches
        object_rectangles_converted, weights = cv.groupRectangles(object_rectangles_converted, 1, 0.5)

        # Creating a list containing center (x, y) coordinates of found matches.
        object_center_xy_coordinates = detection.get_click_points(object_rectangles_converted)

        return object_rectangles_converted, object_center_xy_coordinates

    #--------------------
    # Threading Methods -
    #--------------------

    def start(self):
        self.stopped = False
        t = threading.Thread(target=self.run)
        t.start()


    def stop(self):
        self.stopped = True

    
    def run(self):

        while not self.stopped:

            # Get an updated image of the game
            screenshot = self.gamewindow_capture()

            # Lock the thread while updating the results
            self.lock.acquire()
            self.screenshot = screenshot
            self.lock.release()


#--------------------------------------------------------------------------------------------------------------------


class Object_Detection(Detection):

    # Threading properties
    stopped = True
    lock = None
    rectangles = []
    click_points = []

    # Properties
    screenshot = None
    object_images = []
    object_images_folder_path = []
    method = None

    def __init__(self, needle_img_path, object_images, object_images_folder_path, method=cv.TM_CCOEFF_NORMED):

        # Inheriting from parent class
        super().__init__(needle_img_path, method=cv.TM_CCOEFF_NORMED)

        # Creating a thread lock object
        self.lock = threading.Lock()

        self.object_images = object_images
        self.object_images_folder_path = object_images_folder_path
        self.method = method
        
    
    def update(self, screenshot):

        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()


    def start(self):

        self.stopped = False
        t = threading.Thread(target=self.run)
        t.start()


    def stop(self):
        self.stopped = True


    def run(self):

        while not self.stopped:
            if not self.screenshot is None:
                # Do object detection
                rectangles, click_points = self.detect_object(self.object_images, self.object_images_folder_path)
                # Lock the thread while updating results
                self.lock.acquire()
                self.rectangles = rectangles
                self.click_points = click_points
                self.lock.release()


