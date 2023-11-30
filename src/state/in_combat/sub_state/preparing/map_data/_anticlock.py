class AntiClock:

    @staticmethod
    def get_starting_cells():
        return {
            "3,-25" : [(234, 237), (267, 221), (700, 442), (733, 425)],
            "3,-26" : [(568, 236), (535, 219), (602, 423), (635, 440)],
            "2,-26" : [(400, 186), (434, 169), (633, 272), (667, 289)],
            "2,-27" : [(703, 372), (735, 356), (468, 254), (502, 237)],
            "2,-28" : [(535, 356), (567, 339), (602, 389), (634, 372)],
            "1,-28" : [(266, 323), (300, 306), (433, 408), (467, 424)],
            "1,-27" : [(636, 372), (670, 388), (135, 219), (101, 202)],
            "1,-26" : [(533, 187), (601, 186), (667, 390), (634, 407)],
            "1,-25" : [(601, 458), (567, 474), (601, 288), (667, 288)],
            "2,-25" : [(400, 220), (433, 204), (500, 373), (533, 357)],
            "2,-24" : [(533, 391), (567, 374), (667, 425), (700, 408)],
            "1,-24" : [(467, 390), (500, 374), (200, 254), (234, 237)],
            "0,-24" : [(334, 220), (367, 170), (633, 238), (600, 289)],
            "0,-25" : [(436, 439), (502, 439), (535, 253), (602, 254)],
            "0,-28" : [(469, 457), (536, 456), (636, 236), (770, 236)],
            "-2,-28": [(400, 355), (534, 355), (468, 322), (468, 357)],
            "-2,-26": [(504, 474), (540, 492), (802, 287), (835, 304)],
            "-2,-24": [(468, 319), (500, 305), (567, 305), (434, 373)],
            "-1,-23": [(769, 440), (803, 423), (536, 320), (602, 355)],
            "1,-23" : [(400, 357), (434, 374), (667, 288), (633, 272)],
        }

    @staticmethod
    def get_dummy_cells():
        """
        Used to move character to one of these cells so that the character's
        model doesn't block the view of the starting cells.
        """
        return {
            "0,-25" : [(569, 474), (569, 507), (636, 473), (636, 508), (602, 151), (535, 186), (469, 219), (602, 186)],
            "-2,-28": [(201, 457), (235, 474), (702, 236), (669, 218), (468, 492), (468, 458), (468, 220), (468, 186)],
        }
