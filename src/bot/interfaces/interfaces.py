from ._characteristics import Characteristics
from ._inventory import Inventory
from ._right_click_menu import RightClickMenu
from ._offer_or_invite import OfferOrInvite
from ._main_menu import MainMenu
from ._caution import Caution
from ._information import Information
from ._exceptions import Exceptions


class Interfaces:

    EXCEPTIONS = Exceptions()
    CHARACTERISTICS = Characteristics()
    INVENTORY = Inventory()
    RIGHT_CLICK_MENU = RightClickMenu()
    OFFER_OR_INVITE = OfferOrInvite()
    MAIN_MENU = MainMenu()
    CAUTION = Caution()
    INFORMATION = Information()
