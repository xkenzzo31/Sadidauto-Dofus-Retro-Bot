import os

import cv2

from src.bot._states.in_combat._combat_options._base_option import BaseOption


class SpectatorMode(BaseOption):

    IMAGE_FOLDER_PATH = "src\\bot\\_states\\in_combat\\_combat_options\\_images\\spectator_mode"

    def __init__(self):
        super().__init__(
            name="Spectator Mode",
            on_icon_image_paths=[
                os.path.join(self.IMAGE_FOLDER_PATH, "on_abrak.png"),
                os.path.join(self.IMAGE_FOLDER_PATH, "on_retro.png")
            ],
            off_icon_image_paths=[
                os.path.join(self.IMAGE_FOLDER_PATH, "off_abrak.png"),
                os.path.join(self.IMAGE_FOLDER_PATH, "off_retro.png")
            ]
        )

    def deactivate(self):
        return super()._turn_on(
            is_on=self.is_on,
            get_icon_pos=self._get_icon_pos,
            shrink_turn_bar=False
        )

    def is_on(self):
        return super()._is_on(confidence=0.95, method=cv2.TM_CCORR_NORMED)

    def _get_icon_pos(self):
        return super()._get_icon_pos(confidence=0.89, method=cv2.TM_SQDIFF)
