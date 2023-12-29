class Getter:

    @staticmethod
    def get_data(script: str):
        if "af_" in script:
            return Getter._get_astrub_bank_data()

    @staticmethod
    def _get_astrub_bank_data():
        return {
            "bank_map": "4,-16",
            "zaap_map": "4,-19",
            "no_recall_maps": ["4,-16", "4,-17", "4,-18", "4,-19"],
            "enter_coords": (792, 203),
            "exit_coords": (262, 502),
            "npc_image_folder_path": "src\\bot\\states\\out_of_combat\\sub_state\\banking\\_vault\\images\\astrub_banker_npc"
        }
