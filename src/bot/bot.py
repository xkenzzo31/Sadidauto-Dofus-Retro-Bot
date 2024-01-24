from src.logger import Logger
log = Logger.setup_logger("GLOBAL", Logger.DEBUG, True, True)

import os
import traceback
import threading

from src.image_detection import ImageDetection
from src.screen_capture import ScreenCapture
from src.utilities import load_image_full_path
from src.bot._exceptions import UnrecoverableException, RecoverableException
from src.bot._states.states_enum import State
from src.bot._initializer.initializer import Initializer
from src.bot._states.out_of_combat.controller import Controller as OOC_Controller
from src.bot._states.in_combat.controller import Controller as IC_Controller
from src.bot._recoverer.recoverer import Recoverer


class Bot(threading.Thread):
    """Main bot controller."""

    def __init__(self, script: str, character_name: str, server_name: str):
        super().__init__()
        self.daemon = True
        self._script = script
        self._character_name = character_name
        self._server_name = server_name
        self._state = None
        self._stopped = False
        self._initializer = None
        self._ooc_controller = None
        self._ic_controller = None
        self._recoverer = None

    def run(self):
        try:
            self._initializer = Initializer(self._script, self._character_name)
            self._initializer.initialize()
            self._ooc_controller = OOC_Controller(
                self._set_state, 
                self._script, 
                self._initializer.window_title
            )
            self._ic_controller = IC_Controller(
                self._set_state, 
                self._script, 
                self._character_name
            )
            self._recoverer = Recoverer(
                self._character_name, 
                self._server_name, 
                self._initializer.character_level,
                self._initializer.window_hwnd,
                self._initializer.WINDOW_SIZE
            )
            self._state = self._determine_initial_state()

            while not self._stopped:
                try:
                    if self._state == State.OUT_OF_COMBAT:
                        self._ooc_controller.run()
                    elif self._state == State.IN_COMBAT:
                        self._ic_controller.run()
                except RecoverableException:
                    self._state = self._recoverer.recover()
                    continue

        except UnrecoverableException:
            # ToDo: Implement UnrecoverableException class logic.
            # Take screenshots, logout etc.
            log.critical(traceback.format_exc())
            log.critical("Unrecoverable exception occurred! Exiting ...")
            os._exit(1)
        except Exception:
            log.exception("An unhandled exception occured!")
            log.critical("Exiting ... ")
            os._exit(1)

    def stop(self):
        self._stopped = True

    def _set_state(self, state):
        self._state = state

    @staticmethod
    def _determine_initial_state():
        image = load_image_full_path("src\\bot\\_images\\in_combat_state_verifier.png")
        if len(
            ImageDetection.find_image(
                haystack=ScreenCapture.custom_area((452, 598, 41, 48)), 
                needle=image,
                confidence=0.99,
                mask=ImageDetection.create_mask(image)
            )
        ) > 0:
            log.info(f"Determined initial state: in combat.")
            return State.IN_COMBAT
        log.info(f"Determined initial state: out of combat.")
        return State.OUT_OF_COMBAT
