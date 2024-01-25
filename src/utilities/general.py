import os
from functools import wraps
from time import perf_counter

import cv2
import pyautogui as pyag


def load_image(image_folder_path: str, image_name: str):
    image_path = os.path.join(image_folder_path, image_name)
    if not os.path.exists(image_path):
        raise Exception(f"Path '{image_path}' does not exist.")
    if not os.path.isfile(image_path):
        raise Exception(f"Path '{image_path}' is not a file.")
    return cv2.imread(image_path, cv2.IMREAD_UNCHANGED)


def load_image_full_path(image_path: str):
    if not os.path.exists(image_path):
        raise Exception(f"Path '{image_path}' does not exist.")
    if not os.path.isfile(image_path):
        raise Exception(f"Path '{image_path}' is not a file.")
    return cv2.imread(image_path, cv2.IMREAD_UNCHANGED)


def move_mouse_off_game_area():
    pyag.moveTo(929, 752)


def measure_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = perf_counter()
        result = func(*args, **kwargs)
        end_time = perf_counter()
        print(f"'{func.__name__}' took '{end_time - start_time}' seconds to execute.")
        return result
    return wrapper
