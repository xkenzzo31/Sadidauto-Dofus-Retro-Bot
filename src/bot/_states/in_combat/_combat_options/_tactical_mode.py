import os

import cv2

from src.bot._states.in_combat._combat_options._base_option import BaseOption
from src.utilities.general import load_image
from src.utilities.image_detection import ImageDetection
from src.utilities.screen_capture import ScreenCapture


class TacticalMode(BaseOption):

    IMAGE_FOLDER_PATH = "src\\bot\\_states\\in_combat\\_combat_options\\_images\\tactical_mode"
    ON_TILE_DARKER_IMAGE = load_image(IMAGE_FOLDER_PATH, "on_tile_darker.png")
    ON_TILE_LIGHTER_IMAGE = load_image(IMAGE_FOLDER_PATH, "on_tile_lighter.png")

    def __init__(self):
        super().__init__(
            name="Tactical Mode",
            on_icon_image_paths=[
                os.path.join(self.IMAGE_FOLDER_PATH, "on.png"),
                os.path.join(self.IMAGE_FOLDER_PATH, "on_2.png")
            ],
            off_icon_image_paths=[
                os.path.join(self.IMAGE_FOLDER_PATH, "off.png"),
                os.path.join(self.IMAGE_FOLDER_PATH, "off_2.png")
            ]
        )

    def turn_on(self):
        return super()._turn_on(
            is_on=self.is_on,
            get_icon_pos=self._get_icon_pos,
            shrink_turn_bar=True
        )

    def is_on(self):
        return (
            len(
                ImageDetection.find_images(
                    haystack=ScreenCapture.game_window(),
                    needles=[self.ON_TILE_DARKER_IMAGE, self.ON_TILE_LIGHTER_IMAGE],
                    confidence=0.99,
                    method=cv2.TM_SQDIFF_NORMED
                )
            ) > 0
            and super()._is_on(confidence=0.95, method=cv2.TM_CCORR_NORMED)
        )

    def _get_icon_pos(self):
        return super()._get_icon_pos(confidence=0.98, method=cv2.TM_CCORR_NORMED)


if __name__ == "__main__":
    tactical_mode = TacticalMode()
    print(tactical_mode.is_on())
