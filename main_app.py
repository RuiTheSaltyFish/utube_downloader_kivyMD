from kivymd.app import MDApp
from Screens.main_screen import MainScreen


class MainApp(MDApp):
    def build(self):
        self.title = "Youtube Downloader"
        self.theme_cls.theme_style = "Light"
        return MainScreen()
