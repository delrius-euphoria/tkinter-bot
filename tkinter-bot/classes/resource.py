import json
from utils.paths import RESOURCES_DIR


class Resource:
    def __init__(self):
        with open(RESOURCES_DIR / "tk_info.json") as file:
            self.data = json.load(file)

    def get_all_widgets(self):
        return list(self.data.keys())

    def get_all_tk_wigets(self):
        return [wid for wid in self.get_all_widgets() if wid.startswith("tk.")]

    def get_all_ttk_wigets(self):
        return [
            wid
            for wid in self.get_all_widgets()
            if wid.startswith("ttk") and wid != "ttk"
        ]

    def get_data(self, wid):
        return self.data[wid]

    def get_desc(self, wid):
        return self.data[wid]["desc"]

    def get_code(self, wid):
        return self.data[wid]["code"]

    def get_link(self, wid):
        return self.data[wid]["link"]

    def reload_resource(self):
        self.__init__()
