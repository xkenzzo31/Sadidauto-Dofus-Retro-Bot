from src.logger import get_logger

log = get_logger()

from src.bot._states.in_combat._combat_options.combat_options import CombatOptions
from src.bot._states.in_combat._sub_states.fighting._subsequent_turn_handler._spell_caster import Caster as SpellCaster


class Handler:

    @classmethod
    def handle(cls, character_name: str):
        log.info("Handling subsequent turn actions ...")
        if not SpellCaster.is_any_spell_available():
            log. info("No spells available.")
            return

        if not CombatOptions.TACTICAL_MODE.is_on():
            CombatOptions.TACTICAL_MODE.turn_on()

        if CombatOptions.TURN_BAR.is_shrunk():
            CombatOptions.TURN_BAR.unshrink()

        SpellCaster.cast_spells(character_name)
