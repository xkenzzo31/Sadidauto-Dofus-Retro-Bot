from logger import Logger
log = Logger.setup_logger("GLOBAL", Logger.DEBUG, True, True)

from collections import deque
import os
from time import perf_counter, sleep

import cv2
import pyautogui as pyag

from image_detection import ImageDetection
from screen_capture import ScreenCapture
from src.utilities import load_image
from .map_data import DATA as MAP_DATA


class MapChanger:

    _image_dir_path = "src\\bot\\map_changer\\map_images"
    _map_image_data = {}
    for image_name in [name for name in os.listdir(_image_dir_path) if name.endswith(".png")]:
        _map_image_data[image_name.replace(".png", "")] = load_image(_image_dir_path, image_name)

    map_change_data = MAP_DATA

    @classmethod
    def get_current_map_coords(cls):
        current_map_image = ScreenCapture.custom_area((487, 655, 78, 52))
        for map_coords, map_image in cls._map_image_data.items():
            result = ImageDetection.find_image(
                haystack=map_image,
                needle=current_map_image,
                confidence=0.99,
                method=cv2.TM_SQDIFF_NORMED,
                remove_alpha_channels=True,
            )
            if len(result) > 0:
                return map_coords
        raise ValueError(f"Failed to find current map coords. Perhaps the map image is missing?")

    @classmethod
    def change_map(cls, from_map: str, to_map: str):
        log.info(f"Changing map from '{from_map}' to '{to_map}' ... ")
        if from_map not in cls.map_change_data:
            raise ValueError(f"Data for map coords '{from_map}' not found in MAP_DATA.")
        if to_map not in cls.map_change_data[from_map]:
            raise ValueError(f"Map change (sun) coords for map '{to_map}' not found in '{from_map}' map's data.")
        if cls.map_change_data[from_map][to_map] is None:
            raise ValueError(f"Impossible to change map from '{from_map}' to '{to_map}' because there is no map change (sun) icon in that direction.")
        
        sun_x, sun_y = cls.map_change_data[from_map][to_map]
        pyag.keyDown("e")
        pyag.moveTo(sun_x, sun_y)
        pyag.click()
        pyag.keyUp("e")

    @staticmethod
    def has_loading_screen_passed():
        log.info(f"Waiting for loading screen ... ")
        start_time = perf_counter()
        while perf_counter() - start_time <= 10:
            if MapChanger._is_loading_screen_visible():
                log.info(f"Loading screen detected ... ")
                break
        else:
            log.error(f"Failed to detect loading screen.")
            return False
        
        start_time = perf_counter()
        while perf_counter() - start_time <= 10:
            if not MapChanger._is_loading_screen_visible():
                log.info(f"Loading screen finished.")
                return True
        else:
            log.error(f"Failed to detect end of loading screen.")
            return False

    @staticmethod
    def _is_loading_screen_visible():
        return all((
            pyag.pixelMatchesColor(529, 491, (0, 0, 0)),
            pyag.pixelMatchesColor(531, 429, (0, 0, 0)),
            pyag.pixelMatchesColor(364, 419, (0, 0, 0)),
            pyag.pixelMatchesColor(691, 424, (0, 0, 0))
        ))

    @classmethod
    def get_shortest_path(cls, start, end) -> dict[str, str]: # {from_map: to_map}
        if start not in cls.map_change_data:
            raise ValueError(f"Impossible to generate path from '{start}' to '{end}' because '{start}' is not in MAP_DATA.")
        if end not in cls.map_change_data:
            raise ValueError(f"Impossible to generate path from '{start}' to '{end}' because '{end}' is not in MAP_DATA.")
        if start == end:
            raise ValueError(f"Impossible to generate path from '{start}' to '{end}' because they are the same.")

        queue = deque([(start, [start])])
        visited = set([start])
        while queue:
            node, path = queue.popleft()
            for next_node in cls.map_change_data[node]:
                if next_node == end:
                    path += [next_node]
                    return {path[i]: path[i + 1] for i in range(len(path) - 1)}
                if next_node in cls.map_change_data and next_node not in visited:
                    queue.append((next_node, path + [next_node]))
                    visited.add(next_node)
        
        raise Exception(f"Impossible to generate path from '{start}' to '{end}' because there are no maps conecting them.")
