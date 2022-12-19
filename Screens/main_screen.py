from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivymd.uix.button import MDRaisedButton, MDRectangleFlatButton
from kivymd.uix.gridlayout import MDGridLayout


from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.textfield import MDTextField

from UI_Widget.yt_item import YTItem
from UI_Widget.yt_item_list import YTList
import UI_Widget.Global_Data as gd


class MainScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_field = MDTextField(mode="rectangle", hint_text="Paste URL Here")
        self.get_button = MDRaisedButton(text="Get")
        self.dir_button = MDRectangleFlatButton(text="Download Folder = /download")
        self.get_button.bind(on_press=self.get_utube_video)
        self.dir_button.bind(on_press=self.chose_dir)
        self.yt_list = YTList()
        self.download_dir = "Dir"
        self.pop_up = Popup(title=self.download_dir,
                            title_size=22,
                            size_hint=(None, None), size=(500, 500))
        self.download_button = MDRaisedButton(text="download", on_press=self.download_all_video)
        self.remove_complete = MDRaisedButton(text="Clean", on_press=self.delete_completed)
        self.build_screen()

    def build_screen(self):
        self.add_widget(
            MDGridLayout(
                MDGridLayout(
                    self.url_field,
                    self.get_button,
                    cols=2, spacing=10, adaptive_height=True
                ),
                MDGridLayout(
                    self.dir_button,
                    self.download_button,
                    self.remove_complete,
                    cols=3, spacing=10, adaptive_height=True
                ),
                MDScrollView(
                    self.yt_list,

                ),
                cols=1, padding=20, spacing=10
            )
        )

    def get_utube_video(self, instance):
        try:
            self.yt_list.add_item(YTItem(link=self.url_field.text))
        except Exception:
            Snackbar(
                text="Please check your URL",
                snackbar_x="10dp",
                snackbar_y="10dp",
            ).open()
        finally:
            self.url_field.text = ""

    def chose_dir(self, instance):
        file = FileChooserListView(path="../download")

        file_chooser_pop_up = \
            MDGridLayout(
                file,
                MDRaisedButton(text="OK", on_press=lambda s: self.pop_up_ok(path=file.path),
                               on_release=lambda s: self.pop_up.dismiss()
                               ),
                cols=1,
            )
        self.pop_up.content = file_chooser_pop_up
        self.pop_up.open()

    def pop_up_ok(self, path):
        self.download_dir = path
        self.dir_button.text = "Download Folder = " + path
        gd.download_dir = path

    def download_all_video(self, instance):
        self.yt_list.download_all()

    def delete_completed(self, instance):
        self.yt_list.delete_complete()

