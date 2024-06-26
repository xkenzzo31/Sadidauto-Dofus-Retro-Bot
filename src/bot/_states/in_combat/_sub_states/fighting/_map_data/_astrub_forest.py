class AstrubForest:

    @staticmethod
    def get_movement_data():
        # Format:
        # "map_coords": {"side_color": {(start_cell_x, start_cell_y): (move_to_x, move_to_y)}
        return {
            "2,-24" : {"red": {(533, 391): (533, 391), (567, 374): (567, 374)}, "blue": {(667, 425): (667, 425), (700, 408): (700, 408)}},
            "2,-25" : {"red": {(395, 225): (395, 225), (433, 204): (395, 225)}, "blue": {(500, 373): (466, 358), (533, 357): (466, 358)}},
            "2,-26" : {"red": {(400, 186): (467, 221), (434, 169): (467, 221)}, "blue": {(633, 272): (568, 236), (667, 289): (568, 236)}},
            "3,-26" : {"red": {(568, 236): (532, 290), (435, 236): (532, 290)}, "blue": {(602, 355): (564, 305), (668, 356): (564, 305)}},
            "2,-28" : {"red": {(535, 356): (559, 371), (567, 339): (591, 356)}, "blue": {(602, 389): (559, 371), (634, 372): (591, 356)}},
            "1,-28" : {"red": {(266, 323): (266, 323), (300, 306): (300, 306)}, "blue": {(433, 408): (433, 408), (467, 424): (433, 408)}},
            "1,-25" : {"red": {(535, 425): (635, 374), (602, 423): (635, 374)}, "blue": {(601, 288): (568, 338), (667, 288): (568, 338)}},
            "1,-24" : {"red": {(468, 355): (367, 340), (467, 390): (367, 340)}, "blue": {(169, 271): (267, 289), (234, 237): (267, 289)}},
            "-2,-28": {"red": {(400, 355): (431, 339), (534, 355): (501, 338)}, "blue": {(468, 322): (431, 339), (468, 357): (431, 339)}},
            "-2,-26": {"red": {(535, 492): (636, 441), (468, 424): (568, 441)}, "blue": {(434, 474): (434, 474), (468, 491): (468, 491)}},
            "-2,-24": {"red": {(401, 321): (401, 321), (468, 321): (468, 321)}, "blue": {(435, 372): (435, 372), (568, 304): (568, 304)}},
            "-1,-23": {"red": {(769, 440): (769, 440), (803, 423): (803, 423)}, "blue": {(535, 322): (498, 308), (602, 355): (498, 308)}},
            "1,-23" : {"red": {(400, 357): (400, 357), (434, 374): (434, 374)}, "blue": {(667, 288): (667, 288), (633, 272): (633, 272)}}
        }

    @staticmethod
    def get_starting_cells():
        return {
            "2,-24" : {"red": [(533, 391), (567, 374)], "blue": [(667, 425), (700, 408)]},
            "2,-25" : {"red": [(395, 225), (433, 204)], "blue": [(500, 373), (533, 357)]},
            "2,-26" : {"red": [(400, 186), (434, 169)], "blue": [(633, 272), (667, 289)]},
            "3,-26" : {"red": [(568, 236), (435, 236)], "blue": [(602, 355), (668, 356)]},
            "2,-28" : {"red": [(535, 356), (567, 339)], "blue": [(602, 389), (634, 372)]},
            "1,-28" : {"red": [(266, 323), (300, 306)], "blue": [(433, 408), (467, 424)]},
            "1,-25" : {"red": [(535, 425), (602, 423)], "blue": [(601, 288), (667, 288)]},
            "1,-24" : {"red": [(468, 355), (467, 390)], "blue": [(169, 271), (234, 237)]},
            "-2,-28": {"red": [(400, 355), (534, 355)], "blue": [(468, 322), (468, 357)]},
            "-2,-26": {"red": [(535, 492), (468, 424)], "blue": [(434, 474), (468, 491)]},
            "-2,-24": {"red": [(401, 321), (468, 321)], "blue": [(435, 372), (568, 304)]},
            "-1,-23": {"red": [(769, 440), (803, 423)], "blue": [(535, 322), (602, 355)]},
            "1,-23" : {"red": [(400, 357), (434, 374)], "blue": [(667, 288), (633, 272)]}
        }
