import os
import requests
os.environ["KIVY_NO_CONSOLELOG"] = "1"
os.environ['KIVY_IMAGE'] = 'pil'

from main_app import MainApp
from kivy.core.window import Window

if __name__.endswith('__main__'):
    size = (1000, 900)
    Window.size = size
    MainApp().run()
