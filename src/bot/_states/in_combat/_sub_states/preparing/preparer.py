from src.logger import get_logger

log = get_logger()

import glob
import os
from time import perf_counter

import cv2
import pyautogui as pyag
from PIL import Image

from src.bot._exceptions import RecoverableException
from src.bot._map_changer.map_changer import MapChanger
from src.bot._states.in_combat._combat_options.combat_options import CombatOptions
from src.bot._states.in_combat._status_enum import Status
from src.bot._states.in_combat._sub_states.preparing._exceptions import FailedToSelectDummyCell, FailedToSelectStartingCell
from src.bot._states.in_combat._sub_states.preparing._map_data.getter import Getter as MapDataGetter
from src.bot._states.in_combat._sub_states.sub_states_enum import State as SubState
from src.utilities.general import load_image, load_image_full_path, move_mouse_off_game_area
from src.utilities.image_detection import ImageDetection
from src.utilities.screen_capture import ScreenCapture


class Preparer:

    IMAGE_FOLDER_PATH = "src\\bot\\_states\\in_combat\\_sub_states\\preparing\\_images"
    READY_BUTTON_AREA = (678, 507, 258, 91)
    READY_BUTTON_IMAGES = [
        load_image_full_path(path) 
        for path in glob.glob(os.path.join(IMAGE_FOLDER_PATH, "ready_button\\*.png"))
    ]
    AP_COUNTER_AREA = (452, 598, 41, 48)
    AP_COUNTER_IMAGE = load_image(IMAGE_FOLDER_PATH, "ap_counter_image.png")
    AP_COUNTER_IMAGE_MASK = ImageDetection.create_mask(AP_COUNTER_IMAGE)
    RED = "red"
    BLUE = "blue"

    def __init__(self, script: str, disable_spectator_mode: bool = True):
        self._starting_cell_data = MapDataGetter.get_data_object(script).get_starting_cells()
        self._dummy_cell_data = MapDataGetter.get_data_object(script).get_dummy_cells()
        self._disable_spectator_mode = disable_spectator_mode
        self._did_char_move_to_cell_timeout = 0

    def prepare(self):
        self._did_char_move_to_cell_timeout = 0.35
        try:
            CombatOptions.FIGHT_LOCK.turn_on()
            if self._disable_spectator_mode:
                CombatOptions.SPECTATOR_MODE.deactivate()
            CombatOptions.TACTICAL_MODE.turn_on()

            map_coords = MapChanger.get_current_map_coords()

            attempts = 0
            while attempts < 3:
                # Check if no longer in selection stage. Happens if disconnected
                # or when combat start automatically because the time allowed
                # by Dofus runs out.
                if self._get_ready_button_pos() is None:
                    raise RecoverableException(
                        "Failed to complete cell selection in Preparing state "
                        "because 'Ready' button couldn't be found."
                    )

                try:
                    if self._are_there_any_dummy_cells_on_map(map_coords):
                        final_dummy_cell_color = self._select_dummy_cell(map_coords)
                        # Mouse cursor will stay hovered over the character's model
                        # which in turn will display the black character's info
                        # tooltip (Name (lvl)) that blocks the view of the starting 
                        # cell locations on some maps. The cursor needs to be moved 
                        # off to make sure it doesn't happen.
                        move_mouse_off_game_area()
                        self._select_starting_cell(map_coords, final_dummy_cell_color)
                    else:
                        self._select_starting_cell(map_coords)

                    self._start_combat()
                    return
                except (FailedToSelectDummyCell, FailedToSelectStartingCell):
                    attempts += 1
                    log.info(f"Attempt '{attempts}' to finish preparing failed!")
                    # Cell selection most of the time fails due to Dofus lag
                    # so increasing the timeout allows more time for the
                    # character sprite to move to the cell.
                    self._did_char_move_to_cell_timeout += 1.5

            else:
                raise RecoverableException("Failed to complete cell selection in Preparing state.")                        

        except RecoverableException as e:
            e.occured_in_sub_state = SubState.PREPARING
            raise e

    def _are_there_any_dummy_cells_on_map(self, map_coords: str):
        for map, cell_data in self._dummy_cell_data.items():
            if map == map_coords:
                if len(cell_data[self.RED]) > 0 or len(cell_data[self.BLUE]) > 0:
                    return True
        return False

    def _select_dummy_cell(self, map_coords: str):
        log.info("Selecting a dummy cell ...")

        red_dummy_cells = self._get_free_dummy_cells(self.RED, map_coords)
        blue_dummy_cells = self._get_free_dummy_cells(self.BLUE, map_coords)

        for cell_coords in red_dummy_cells:
            if self._move_char_to_cell(*cell_coords) == Status.SUCCESSFULLY_MOVED_TO_CELL:
                log.info(f"Successfully selected red side dummy cell: {cell_coords}.")
                return self.RED
        for cell_coords in blue_dummy_cells:
            if self._move_char_to_cell(*cell_coords) == Status.SUCCESSFULLY_MOVED_TO_CELL:
                log.info(f"Successfully selected blue side dummy cell: {cell_coords}.")
                return self.BLUE
        
        if len(red_dummy_cells) == 0:
            return self.RED
        elif len(blue_dummy_cells) == 0:
            return self.BLUE
        
        raise FailedToSelectDummyCell("Failed to select a dummy cell.")

    def _select_starting_cell(self, map_coords: str, dummy_cell_color: str = None):
        log.info("Selecting a starting cell ...")

        if dummy_cell_color is not None:
            starting_cells = self._get_free_starting_cells(dummy_cell_color, map_coords)
        else:
            red_starting_cells = self._get_free_starting_cells(self.RED, map_coords)
            blue_starting_cells = self._get_free_starting_cells(self.BLUE, map_coords)
            starting_cells = red_starting_cells + blue_starting_cells

        for cell_coords in starting_cells:
            if self._move_char_to_cell(*cell_coords) == Status.SUCCESSFULLY_MOVED_TO_CELL:
                log.info(f"Successfully selected starting cell: {cell_coords}.")
                return
        
        raise FailedToSelectStartingCell("Failed to select a starting cell.")

    def _start_combat(self):
        log.info("Starting combat ... ")
        ready_button_pos = self._get_ready_button_pos()
        if ready_button_pos is None:
            raise RecoverableException("Failed to get ready button position.")
        
        pyag.moveTo(*ready_button_pos)
        pyag.click()
        move_mouse_off_game_area()

        timeout = 5
        start_time = perf_counter()
        while perf_counter() - start_time <= timeout:
            if self._is_ap_counter_visible():
                log.info("Successfully started combat.")
                return

        raise RecoverableException(f"Failed to detect the start of combat. Timed out: {timeout} seconds.")
    
    def _move_char_to_cell(self, cell_x, cell_y):
        px_color_before_clicking_cell = pyag.pixel(cell_x, cell_y)
        self._click_cell(cell_x, cell_y)
        if self._did_char_move(cell_x, cell_y, px_color_before_clicking_cell):
            return Status.SUCCESSFULLY_MOVED_TO_CELL
        return Status.FAILED_TO_MOVE_TO_CELL

    def _get_dummy_cells(self, map_coords: str, color: str):
        if color not in [self.RED, self.BLUE]:
            raise ValueError(f"Invalid cell color: '{color}'.")
        for map, cell_data in self._dummy_cell_data.items():
            if map == map_coords:
                return cell_data[color]
        return []

    def _get_free_dummy_cells(self, map_coords: str, color: str):
        free_cells = []
        for cell_coords in self._get_dummy_cells(color, map_coords):
            game_window_screenshot = pyag.screenshot(region=ScreenCapture.GAME_WINDOW_AREA)
            if self._is_cell_free(*cell_coords, game_window_screenshot):
                free_cells.append(cell_coords)
        return free_cells

    def _get_starting_cells(self, map_coords: str, color: str):
        if color not in [self.RED, self.BLUE]:
            raise ValueError(f"Invalid cell color: '{color}'.")
        for map, cell_data in self._starting_cell_data.items():
            if map == map_coords:
                return cell_data[color]
        return []
    
    def _get_free_starting_cells(self, map_coords: str, color: str):
        free_cells = []
        for cell_coords in self._get_starting_cells(color, map_coords):
            game_window_screenshot = pyag.screenshot(region=ScreenCapture.GAME_WINDOW_AREA)
            if self._is_cell_free(*cell_coords, game_window_screenshot):
                free_cells.append(cell_coords)
        return free_cells

    def _did_char_move(self, cell_x, cell_y, px_color_before_moving: tuple):
        start_time = perf_counter()
        while perf_counter() - start_time <= self._did_char_move_to_cell_timeout:
            if (
                not pyag.pixelMatchesColor(cell_x, cell_y, px_color_before_moving)
                and not self._is_cell_free(cell_x, cell_y, pyag.screenshot(region=(0, 0, 933, 600)))
            ):
                return True
        return False
    
    def _get_ready_button_pos(self):
        rectangles = ImageDetection.find_images(
            haystack=ScreenCapture.custom_area(self.READY_BUTTON_AREA),
            needles=self.READY_BUTTON_IMAGES,
            confidence=0.99,
            method=cv2.TM_SQDIFF
        )
        if len(rectangles) > 0:
            return ImageDetection.get_rectangle_center_point((
                rectangles[0][0] + self.READY_BUTTON_AREA[0],
                rectangles[0][1] + self.READY_BUTTON_AREA[1],
                rectangles[0][2],
                rectangles[0][3]
            ))
        return None
    
    def _is_ap_counter_visible(self):
        return len(
            ImageDetection.find_image(
                haystack=ScreenCapture.custom_area(self.AP_COUNTER_AREA),
                needle=self.AP_COUNTER_IMAGE,
                confidence=0.99,
                mask=self.AP_COUNTER_IMAGE_MASK
            )
        ) > 0

    @staticmethod
    def _is_cell_free(cell_x, cell_y, game_window_screenshot: Image.Image):
        if game_window_screenshot is None:
            game_window_screenshot = pyag.screenshot(region=ScreenCapture.GAME_WINDOW_AREA)
        colors = [
            # There are multiple shades of red and blue because on some maps
            # the "You started a fight!" message makes the cell colors a 
            # bit darker.
            (255, 0, 0), (154, 0, 0), (77, 0, 0), (38, 0, 0), (179, 0, 0),
            (0, 0, 255), (0, 0, 154), (0, 0, 179)
        ]
        for color in colors:
            if game_window_screenshot.getpixel((cell_x, cell_y)) == color:
                return True
        return False

    @staticmethod
    def _click_cell(cell_x, cell_y):
        pyag.moveTo(cell_x, cell_y)
        pyag.click()


if __name__ == "__main__":
    preparer = Preparer("af_anticlock")
    preparer.prepare()
