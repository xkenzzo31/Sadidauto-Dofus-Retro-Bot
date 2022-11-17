"""Holds various data classes."""

#----------------------------------------------------------------------#
#---------------------------DETECTION RELATED--------------------------#
#----------------------------------------------------------------------#


class ImageData:
    """Holds image data."""

    # Test images.
    test_monster_images_path = "images\\test_monster_images\\"
    test_monster_images_list = ["test_1.png"]

    # Status images.
    # Path to folder.
    s_i = "images\\status_images\\"
    # Verifiers.
    end_of_combat_v_1 = "END_OF_COMBAT_verifier_1.jpg"
    fighting_sv_1 = "FIGHTING_state_verifier_1.jpg"
    fighting_sv_2 = "FIGHTING_state_verifier_2.jpg"
    fighting_sv_3 = "FIGHTING_state_verifier_3.jpg"
    preparing_sv_1 = "PREPARING_state_verifier_1.jpg"
    preparing_sv_2 = "PREPARING_state_verifier_2.jpg"

    # Bank images.
    bank_images_path = "images\\bank_images\\"
    empty_bank_slot = bank_images_path + "empty_bank_slot.jpg"

    # Interface images.
    interface_images_path = "images\\interface_images\\"
    dofus_logo = interface_images_path + "dofus_logo.jpg"

    class AstrubForest:
        """Holds 'Astrub Forest' script image data."""
        
        # Monster images and path.
        monster_img_path = "images\\monster_images\\astrub_forest\\"
        monster_img_list = [
            "Boar_BL_1.png", "Boar_BR_1.png", "Boar_TL_1.png", "Boar_TR_1.png",

            "Pres_BL_1.png", "Pres_BR_1.png", "Pres_TL_1.png", "Pres_TR_1.png",
            "Pres_BL_2.png", "Pres_BR_2.png",

            "Mosk_BL_1.png", "Mosk_BR_1.png", "Mosk_TL_1.png", "Mosk_TR_1.png",
            "Mosk_BR_2.png", "Mosk_BL_2.png",

            "Mush_BL_1.png", "Mush_BR_1.png", "Mush_TL_1.png", "Mush_TR_1.png",
            "Mush_BL_2.png", "Mush_BR_2.png", "Mush_TL_2.png", "Mush_TR_2.png",

            "Wolf_BL_1.png", "Wolf_BR_1.png", "Wolf_TL_1.png", "Wolf_TR_1.png",
        ]

        # Astrub banker NPC images and path.
        banker_images_path = "images\\npc_images\\astrub_banker\\"
        banker_images_list = [
            "bnkr_BL_1.jpg", "bnkr_BR_1.jpg", "bnkr_TL_1.jpg","bnkr_TR_1.jpg",
            "bnkr_BL_2.jpg", "bnkr_BR_2.jpg", "bnkr_TL_2.jpg","bnkr_TR_2.jpg",
            "bnkr_BL_3.jpg", "bnkr_BR_3.jpg", "bnkr_TL_3.jpg","bnkr_TR_3.jpg",
            "bnkr_BL_4.jpg", "bnkr_BR_4.jpg", "bnkr_TL_4.jpg","bnkr_TR_4.jpg",
        ]

#----------------------------------------------------------------------#
#---------------------------MOVEMENT RELATED---------------------------#
#----------------------------------------------------------------------#


class MapData:
    """
    Holds map data.
    
    - When adding cell coordinates to maps, the first two coordinates 
    must be red color cells and the last two must be blue. A total of 
    4 cells is accepted. 
    - Character must be highlighted (white) when the coordinates 
    (of cells) are clicked/hovered on. This makes script able to check
    whether character was moved. Make sure character is highlighted 
    both mounted and not.
    - Select cell coordinates that cannot be blocked by random 
    char/monster placement when joining fight. The blue/red pixel 
    on the cell coordinate must be visible during selection.

    Map types
    ----------
    - Fightable - character will search for monsters and fight on it.
    - Traversable - character will run through it without fighting.
    
    """

    class AstrubForest:
        """'Astrub Forest' script map data."""

        # Map data for hunting mobs.
        hunting = [
            # 'Astrub Bank' map.
            {"4,-16" : {"top"   : (467, 87),  "map_type": "traversable"}},
            {"4,-17" : {"top"   : (434, 71),  "map_type": "traversable"}},
            {"4,-18" : {"top"   : (499, 70),  "map_type": "traversable"}},
            {"4,-19" : {"top"   : (501, 69),  "map_type": "traversable"}},
            {"4,-20" : {"top"   : (433, 70),  "map_type": "traversable"}},
            {"4,-21" : {"right" : (901, 376), "map_type": "traversable"}},
            {"5,-21" : {"top"   : (367, 69),  "map_type": "traversable"}},
            {"5,-22" : {"top"   : (566, 69),  "map_type": "traversable"}},
            {"5,-23" : {"left"  : (34, 342),  "map_type": "traversable"}},
            {"4,-23" : {"left"  : (33, 307),  "map_type": "traversable"}},
            {"3,-23" : {"top"   : (434, 69),  "map_type": "traversable"}},
            {"3,-24" : {"top"   : (299, 69),  "map_type": "traversable"}},
            {"3,-25" : {"top"   : (500, 56),  "map_type": "fightable",
                        "cell"  : [(234, 237),(267, 221),(700, 442),(733, 425)]}},
            {"3,-26" : {"left"  : (8, 342),   "map_type": "fightable",
                        "cell"  : [(568, 236),(535, 219),(602, 423),(635, 440)]}},
            {"2,-26" : {"top"   : (300, 56),  "map_type": "fightable",
                        "cell"  : [(400, 186),(434, 169),(633, 272),(667, 289)]}},
            {"2,-27" : {"top"   : (567, 70),  "map_type": "traversable"}},
            {"2,-28" : {"left"  : (8, 443),   "map_type": "fightable",
                        "cell"  : [(535, 356),(567, 339),(602, 389),(634, 372)]}},
            {"1,-28" : {"bottom": (367, 580),  "map_type": "fightable",
                        "cell"  : [(266, 323),(300, 306),(433, 408),(467, 424)]}},
            {"1,-27" : {"bottom": (566, 580), "map_type": "traversable"}},
            {"1,-26" : {"bottom": (633, 580), "map_type": "fightable",
                        "cell"  : [(533, 187),(601, 186),(667, 390),(634, 407)]}},
            {"1,-25" : {"right" : (926, 443), "map_type": "fightable",
                        "cell"  : [(601, 458),(567, 474),(601, 288),(667, 288)]}},
            {"2,-25" : {"bottom": (567, 580), "map_type": "fightable",
                        "cell"  : [(400, 220),(433, 204),(500, 373),(533, 357)]}},
            {"2,-24" : {"left"  : (8, 307),   "map_type": "fightable",
                        "cell"  : [(533, 391),(567, 374),(667, 425),(700, 408)]}},
            {"1,-24" : {"left"  : (8, 342),   "map_type": "fightable",
                        "cell"  : [(467, 390),(500, 374),(200, 254),(234, 237)]}},
            {"0,-24" : {"top"   : (434, 56),  "map_type": "fightable",
                        "cell"  : [(334, 220),(367, 170),(633, 238),(600, 289)]}},
            {"0,-25" : {"left"  : (32, 308),  "map_type": "traversable"}},
            {"-1,-25": {"top"   : (433, 71),  "map_type": "traversable"}},
            {"-1,-26": {"left"  : (33, 341),  "map_type": "traversable"}},
            {"-2,-26": {"bottom": (433, 581), "map_type": "fightable",
                        "cell"  : [(504, 474),(540, 492),(802, 287),(835, 304)]}},
            {"-2,-25": {"bottom": (500, 582), "map_type": "traversable"}},
            {"-2,-24": {"right" : (926, 309), "map_type": "fightable",
                        "cell"  : [(468, 319),(500, 305),(567, 305),(434, 373)]}},
            {"-1,-24": {"bottom": (433, 579), "map_type": "traversable"}},
            {"-1,-23": {"right" : (926, 274), "map_type": "fightable",
                        "cell"  : [(769, 440),(803, 423),(536, 320),(602, 355)]}},
            {"0,-23" : {"right" : (901, 343), "map_type": "traversable"}},
            {"1,-23" : {"right" : (926, 410), "map_type": "fightable",
                        "cell"  : [(400, 357),(434, 374),(667, 288),(633, 272)]}},
            {"2,-23" : {"right" : (901, 308), "map_type": "traversable"}},
            # Used only when map was changed accidentally during attack.
            {"-1,-22" : {"top"   : (500, 56),  "map_type": "traversable"}},
            {"-2,-23" : {"top"   : (500, 55),  "map_type": "traversable"}},
            {"-3,-24" : {"right" : (930, 308), "map_type": "traversable"}},
            {"-3,-26" : {"right" : (930, 308), "map_type": "traversable"}},
            {"-2,-27" : {"bottom": (433, 593), "map_type": "traversable"}},
            {"0,-26"  : {"right" : (928, 411), "map_type": "traversable"}},
            {"0,-28"  : {"right" : (927, 240), "map_type": "traversable"}},
            {"2,-29"  : {"bottom": (493, 588), "map_type": "traversable"}},
            {"3,-28"  : {"left"  : (5, 342),   "map_type": "traversable"}},
            {"3,-27"  : {"bottom": (700, 592), "map_type": "traversable"}},
            {"4,-26"  : {"left"  : (4, 377),   "map_type": "traversable"}},
            {"4,-25"  : {"left"  : (8, 408),   "map_type": "traversable"}},
        ]

        # Map data for hunting mobs (different pathing).
        hunting_reversed = [
            # 'Astrub Bank' map.
            {"4,-16" : {"left"  : (33, 341),  "map_type": "traversable"}},
            {"3,-16" : {"left"  : (32, 274),  "map_type": "traversable"}},
            {"2,-16" : {"left"  : (33, 342),  "map_type": "traversable"}},
            {"1,-16" : {"left"  : (31, 274),  "map_type": "traversable"}},
            {"0,-16" : {"top"   : (300, 70),  "map_type": "traversable"}},
            {"0,-17" : {"top"   : (500, 70),  "map_type": "traversable"}},
            {"0,-18" : {"top"   : (432, 70),  "map_type": "traversable"}},
            {"0,-19" : {"top"   : (434, 70),  "map_type": "traversable"}},
            {"0,-20" : {"left"  : (31, 308),  "map_type": "traversable"}},
            {"-1,-20": {"left"  : (32, 376),  "map_type": "traversable"}},
            {"-2,-20": {"top"   : (500, 70),  "map_type": "traversable"}},
            {"-2,-21": {"top"   : (500, 70),  "map_type": "traversable"}},
            {"-2,-22": {"top"   : (500, 70),  "map_type": "traversable"}},
            {"-2,-23": {"top"   : (500, 70),  "map_type": "traversable"}},
            {"-2,-24": {"top"   : (432, 56),  "map_type": "fightable",
                        "cell"  : [(468, 319),(500, 305),(567, 305),(434, 373)]}},
            {"-2,-25": {"top"   : (501, 66),  "map_type": "traversable"}},
            {"-2,-26": {"right" : (926, 306), "map_type": "fightable",
                        "cell"  : [(504, 474),(540, 492),(802, 287),(835, 304)]}},
            {"-1,-26": {"bottom": (433, 580), "map_type": "traversable"}},
            {"-1,-25": {"right" : (900, 307), "map_type": "traversable"}},
            {"0,-25" : {"bottom": (433, 583), "map_type": "traversable"}},
            {"0,-24" : {"right" : (926, 341), "map_type": "fightable",
                        "cell"  : [(334, 220),(367, 170),(633, 238),(600, 289)]}},
            {"1,-24" : {"right" : (929, 308), "map_type": "fightable",
                        "cell"  : [(467, 390),(500, 374),(200, 254),(234, 237)]}},
            {"2,-24" : {"top"   : (568, 57),  "map_type": "fightable",
                        "cell"  : [(533, 391),(567, 374),(667, 425),(700, 408)]}},
            {"2,-25" : {"left"  : (7, 444),   "map_type": "fightable",
                        "cell"  : [(400, 220),(433, 204),(500, 373),(533, 357)]}},
            {"1,-25" : {"top"   : (635, 56),  "map_type": "fightable",
                        "cell"  : [(601, 458),(567, 474),(601, 288),(667, 288)]}},
            {"1,-26" : {"top"   : (568, 56),  "map_type": "fightable",
                        "cell"  : [(533, 187),(601, 186),(667, 390),(634, 407)]}},
            {"1,-27" : {"top"   : (367, 70),  "map_type": "traversable"}},
            {"1,-28" : {"right" : (927, 442), "map_type": "fightable",
                        "cell"  : [(266, 323),(300, 306),(433, 408),(467, 424)]}},
            {"2,-28" : {"bottom": (567, 581), "map_type": "fightable",
                        "cell"  : [(535, 356),(567, 339),(602, 389),(634, 372)]}},
            {"2,-27" : {"bottom": (300, 580), "map_type": "traversable"}},
            {"2,-26" : {"right" : (928, 341), "map_type": "fightable",
                        "cell"  : [(400, 186),(434, 169),(633, 272),(667, 289)]}},
            {"3,-26" : {"bottom": (500, 580), "map_type": "fightable",
                        "cell"  : [(568, 236),(535, 219),(602, 423),(635, 440)]}},
            {"3,-25" : {"bottom": (300, 580), "map_type": "fightable",
                        "cell"  : [(234, 237),(267, 221),(700, 442),(733, 425)]}},
            {"3,-24" : {"bottom": (433, 581), "map_type": "traversable"}},
            {"3,-23" : {"left"  : (32, 308),  "map_type": "traversable"}},
            {"2,-23" : {"left"  : (32, 409),  "map_type": "traversable"}},
            {"1,-23" : {"left"  : (7, 307),   "map_type": "fightable",
                        "cell"  : [(400, 357),(434, 374),(667, 288),(633, 272)]}},
            {"0,-23" : {"left"  : (32, 308),  "map_type": "traversable"}},
            {"-1,-23": {"left"  : (7, 307),   "map_type": "fightable",
                        "cell"  : [(769, 440),(803, 423),(536, 320),(602, 355)]}},
            # Used only when map was changed accidentally during attack.
            {"-1,-22" : {"top"   : (500, 56),  "map_type": "traversable"}},
            {"-1,-24" : {"left"  : (33, 342),  "map_type": "traversable"}},
            {"-3,-24" : {"right" : (930, 308), "map_type": "traversable"}},
            {"-3,-26" : {"right" : (930, 308), "map_type": "traversable"}},
            {"-2,-27" : {"bottom": (433, 593), "map_type": "traversable"}},
            {"0,-26"  : {"right" : (928, 411), "map_type": "traversable"}},
            {"0,-28"  : {"right" : (927, 240), "map_type": "traversable"}},
            {"2,-29"  : {"bottom": (493, 588), "map_type": "traversable"}},
            {"3,-28"  : {"left"  : (5, 342),   "map_type": "traversable"}},
            {"3,-27"  : {"bottom": (700, 592), "map_type": "traversable"}},
            {"4,-26"  : {"left"  : (4, 377),   "map_type": "traversable"}},
            {"4,-25"  : {"left"  : (8, 408),   "map_type": "traversable"}},
        ]

        # Map data for banking.
        banking = [
            {"4,-16"  : {}},
            {"4,-17"  : {"bottom" : (433, 580)}},
            {"4,-18"  : {"bottom" : (367, 580)}},
            {"4,-19"  : {"bottom" : (433, 580)}},    
            {"4,-20"  : {"bottom" : (500, 580)}},  
            {"4,-21"  : {"bottom" : (367, 580)}},
            {"5,-21"  : {"left"   : (32, 273) }},
            {"5,-22"  : {"bottom" : (367, 580)}},
            {"5,-23"  : {"bottom" : (567, 580) }},
            {"4,-23"  : {"right"  : (900, 342)}},
            {"3,-23"  : {"right"  : (900, 307)}},
            {"3,-24"  : {"bottom" : (433, 580)}},
            {"3,-25"  : {"bottom" : (300, 580)}},
            {"3,-26"  : {"bottom" : (500, 580)}},
            {"3,-27"  : {"bottom" : (700, 580)}},
            {"1,-28"  : {"right"  : (900, 444)}},
            {"2,-28"  : {"bottom" : (566, 580)}},
            {"1,-27"  : {"right"  : (920, 240)}},
            {"2,-27"  : {"right"  : (901, 343)}},
            {"1,-26"  : {"right"  : (901, 342)}},
            {"2,-26"  : {"right"  : (901, 342)}},
            {"-1,-26" : {"left"   : (31, 342), "bottom" : (433, 580)}},
            {"-1,-25" : {"left"   : (33, 308), "right"  : (901, 309)}},
            {"0,-25"  : {"right"  : (900, 409)}},
            {"1,-25"  : {"right"  : (901, 444)}},
            {"2,-25"  : {"right"  : (901, 274)}},
            {"0,-25"  : {"right"  : (900, 409)}},
            {"-1,-24" : {"left"   : (33, 342), "right"  : (900, 294)}},
            {"0,-24"  : {"right"  : (901, 341)}},
            {"1,-24"  : {"right"  : (900, 308)}},       
            {"2,-24"  : {"right"  : (900, 376)}},     
            {"-1,-23" : {"left"   : (33, 308), "right"  : (901, 274)}},
            {"0,-23"  : {"right"  : (900, 342)}},   
            {"1,-23"  : {"right"  : (900, 409)}},   
            {"2,-23"  : {"right"  : (900, 308)}},   
            {"-2,-26" : {"bottom" : (433, 580)}},
            {"-2,-25" : {"bottom" : (500, 580)}},
            {"-2,-24" : {"bottom" : (433, 580)}},
            {"-2,-23" : {"bottom" : (500, 580)}},
            {"-2,-22" : {"bottom" : (567, 580)}},
            {"-2,-21" : {"bottom" : (500, 580)}},
            {"-2,-20" : {"right"  : (900, 410)}},
            {"-1,-20" : {"right"  : (900, 342)}},
            {"0,-20"  : {"right"  : (900, 308)}},
            {"1,-20"  : {"right"  : (900, 376)}},
            {"2,-20"  : {"right"  : (900, 309)}},
            {"3,-20"  : {"right"  : (900, 376)}},
        ]


#----------------------------------------------------------------------#
#----------------------------COMBAT RELATED----------------------------#
#----------------------------------------------------------------------#


class CombatData:
    """Holds combat related data."""

    images_path = "images\\combat_images\\"
    icon_turn_pass = images_path + "icon_turn_pass.jpg"

    class Spell:
        """
        Holds spell data.
        
        Format
        ----------
        If value of 'e', 'p' or 's' is ONLY a tuple:
            (coordinates to click on to cast spell)
        If value of 'e', 'p' or 's' is a dictionary:
            {(start cell coordinates): (coords to click on to cast spell)}

        """

        # Spell paths.
        images_path = "images\\combat_images\\"
        e_quake = images_path + "earthquake.jpg"
        p_wind = images_path + "poisoned_wind.jpg"
        s_power = images_path + "sylvan_power.jpg"
        spells = [e_quake, p_wind, s_power]

        class AstrubForest:
            """Spell cast data for 'Astrub Forest' scripts."""

            af = [
                {"3,-25" : {"r": {"e": {(234, 237): (466, 359),
                                        (267, 221): (499, 342)},
                                  "p": {(234, 237): (466, 359),
                                        (267, 221): (499, 342)},
                                  "s": {(234, 237): (365, 308),
                                        (267, 221): (400, 291)}},
                            "b": {"e": {(700, 442): (464, 325),
                                        (733, 425): (496, 306)},
                                  "p": {(700, 442): (464, 325),
                                        (733, 425): (496, 306)},
                                  "s": {(700, 442): (567, 375),
                                        (733, 425): (597, 358)}}}},
                {"3,-26" : {"r": {"e": (532, 290), "p": (532, 290), "s": (532, 290)},
                            "b": {"e": (599, 322), "p": (599, 322), "s": (499, 374)}}},
                {"2,-26" : {"r": {"e": (499, 240), "p": (499, 240), "s": (499, 240)},
                            "b": {"e": (531, 223), "p": (531, 223), "s": (531, 223)}}},
                {"2,-28" : {"r": {"e": (632, 407), "p": (632, 407), "s": (527, 361)},
                            "b": {"e": (498, 341), "p": (498, 341), "s": (593, 393)}}},
                {"1,-28" : {"r": {"e": (260, 326), "p": (260, 326), "s": (260, 326)},
                            "b": {"e": (427, 409), "p": (427, 409), "s": (427, 409)}}},
                {"1,-26" : {"r": {"e": (498, 308), "p": (498, 308), "s": (599, 257)},
                            "b": {"e": (667, 288), "p": (667, 288), "s": (766, 341)}}},
                {"1,-25" : {"r": {"e": (599, 359), "p": (599, 359), "s": (698, 408)},
                            "b": {"e": (665, 358), "p": (665, 358), "s": (665, 358)}}},
                {"2,-25" : {"r": {"e": (395, 225), "p": (395, 225), "s": (395, 225)},
                            "b": {"e": (399, 323), "p": (399, 323), "s": (494, 376)}}},
                {"2,-24" : {"r": {"e": (527, 393), "p": (527, 393), "s": (527, 393)},
                            "b": {"e": (660, 428), "p": (660, 428), "s": (660, 428)}}},
                {"1,-24" : {"r": {"e": (366, 342), "p": (366, 342), "s": (461, 394)},
                            "b": {"e": (299, 308), "p": (299, 308), "s": (194, 257)}}},
                {"0,-24" : {"r": {"e": (531, 291), "p": (531, 291), "s": (432, 239)},
                            "b": {"e": (399, 188), "p": (399, 188), "s": (499, 239)}}},
                {"-2,-26": {"r": {"e": (598, 426), "p": (598, 426), "s": (504, 474)},
                            "b": {"e": (599, 393), "p": (599, 393), "s": (699, 341)}}},
                {"-2,-24": {"r": {"e": (461, 325), "p": (461, 325), "s": (461, 325)},
                            "b": {"e": {(567, 305): (560, 308),
                                        (434, 373): (427, 376)},
                                  "p": {(567, 305): (560, 308),
                                        (434, 373): (427, 376)},
                                  "s": {(567, 305): (560, 308),
                                        (434, 373): (427, 376)}}}},
                {"-1,-23": {"r": {"e": (761, 445), "p": (761, 445), "s": (761, 445)},
                            "b": {"e": (498, 308), "p": (498, 308), "s": (498, 308)}}},
                {"1,-23" : {"r": {"e": (394, 360), "p": (394, 360), "s": (394, 360)},
                            "b": {"e": (661, 291), "p": (661, 291), "s": (661, 291)}}},
            ]


    class Movement:
        """
        Holds data for in-combat movement.
        
        Format
        ----------
        If value of 'red' or 'blue' is ONLY a tuple:
            (x, y coordinates of starting cell)
        If value of 'red' or 'blue' is a dictionary:
            {(x, y coordinates of starting cell): (coordinates to click on)}
        
        """

        class AstrubForest:
            """In-combat movement data for 'Astrub Forest' scripts."""

            af = [
                {"3,-25" : {"red" : {(234, 237): (365, 308),
                                     (267, 221): (400, 291)},
                            "blue": {(700, 442): (567, 375),
                                     (733, 425): (597, 358)}}},
                {"3,-26" : {"red" : (532, 290), "blue": (499, 374)}},
                {"2,-26" : {"red" : (499, 240), "blue": (531, 223)}},
                {"2,-28" : {"red" : (525, 358), "blue": (594, 393)}},
                {"1,-28" : {"red" : (260, 326), "blue": (427, 409)}},
                {"1,-26" : {"red" : (599, 257), "blue": (766, 342)}},
                {"1,-25" : {"red" : (698, 408), "blue": (665, 358)}},
                {"2,-25" : {"red" : (395, 225), "blue": (494, 376)}},
                {"2,-24" : {"red" : (527, 393), "blue": (660, 428)}},
                {"1,-24" : {"red" : (461, 394), "blue": (194, 257)}},
                {"0,-24" : {"red" : (432, 239), "blue": (499, 239)}},       
                {"-2,-26": {"red" : (504, 474), "blue": (699, 341)}},
                {"-2,-24": {"red" : (461, 325), 
                            "blue": {(567, 305): (560, 308),
                                     (434, 373): (427, 376)}}},
                {"-1,-23": {"red" : (761, 445), "blue": (498, 308)}},
                {"1,-23" : {"red" : (394, 360), "blue": (661, 291)}},
            ]
