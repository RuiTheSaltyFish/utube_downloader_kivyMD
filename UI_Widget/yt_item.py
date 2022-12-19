import os
from enum import Enum


from kivy.uix.image import *
from kivymd.material_resources import dp
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from pytube import YouTube
import threading
import UI_Widget.Global_Data as gd


class DownloadStatus(Enum):
    pending = 0
    downloading = 1
    complete = 2


class YTItem:
    def __init__(self, link: str):
        self.yt = YouTube(link)
        self.resolution_dropdown = MDDropDownItem(size_hint=(None, None), pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.resolution_dropdown.text = "Video"
        self.resolution_menu: MDDropdownMenu = MDDropdownMenu()
        self.resolution_dropdown.bind(on_press=lambda s: self.resolution_menu.open())
        self.target = "Video"
        self.download_button = MDRaisedButton(text="download",
                                              on_release=lambda s: self.start_download_thread(
                                                  gd.download_dir))
        self.delete_status = 0
        self.download_status = DownloadStatus.pending
        self.box_card = MDBoxLayout(adaptive_height=True,padding=5)

    def set_res(self, res: str):
        self.target = res
        self.resolution_dropdown.text = res
        self.resolution_menu.dismiss()

    def build_widget(self) -> MDBoxLayout:
        self.resolution_menu = MDDropdownMenu(
            caller=self.resolution_dropdown,
            items=[{
                "viewclass": "OneLineListItem",
                "height": dp(56),
                "text": "Video",
                "on_release": lambda: self.set_res("Video"),
            },
                {
                    "viewclass": "OneLineListItem",
                    "height": dp(56),
                    "text": "Sound",
                    "on_release": lambda: self.set_res("Sound"),
                },
                {
                    "viewclass": "OneLineListItem",
                    "height": dp(56),
                    "text": "1080p",
                    "on_release": lambda: self.set_res("1080p"),
                }
            ],

            position="center",
            width_mult=4,
        )

        self.box_card.add_widget(
            MDCard(
                MDGridLayout(
                    AsyncImage(source=self.yt.thumbnail_url),
                    MDLabel(text=self.yt.title),
                    MDAnchorLayout(
                        self.resolution_dropdown,
                        anchor_y="center",
                        anchor_x="left",
                        size_hint_x=.9
                    ),
                    MDAnchorLayout(
                        self.download_button,
                        anchor_y="center",
                        anchor_x="left",
                        size_hint_x=.9
                    ),
                    MDAnchorLayout(
                        MDIconButton(icon="delete", theme_text_color="Custom", text_color="red",
                                     on_press=lambda s: self.delete()),
                        anchor_y="center",
                        anchor_x="left",
                        size_hint_x=.9
                    ),
                    cols=5, spacing=30
                ),
                style="outlined", size_hint_y=None, size=("0dp", "225dp"), padding=10, line_color=(0.2, 0.2, 0.2, 0.2),shadow_softness=2
            )
        )
        return self.box_card

    def download(self, out_folder: str):
        if self.yt is not None and self.download_status == DownloadStatus.pending:
            self.download_status = DownloadStatus.downloading

            if self.target == "Video":
                video_source = self.yt.streams.get_highest_resolution()
                video_source.download(output_path=out_folder)
                self.download_button.text = "Completed"
                self.download_button.disabled_color = "green"

            if self.target == "Sound":
                audio_source = self.yt.streams.get_audio_only()
                result = audio_source.download(output_path=out_folder)
                base, ext = os.path.splitext(result)
                new_file = base + '.mp3'
                os.rename(result, new_file)
                self.download_button.text = "Completed"
                self.download_button.disabled_color = "green"

            if self.target == "1080p":
                video_source = self.yt.streams.filter(resolution="1080p", mime_type="video/webm").first().download(
                    output_path=out_folder)
                audio_source = self.yt.streams.get_audio_only().download(filename_prefix="audio_",
                                                                         output_path=out_folder)
                v_clip = VideoFileClip(video_source)
                a_clip = AudioFileClip(audio_source)
                m_clip = v_clip.set_audio(a_clip)
                m_clip.write_videofile(self.yt.title + "1080p")
                os.remove(video_source)
                os.remove(audio_source)
            self.download_status = DownloadStatus.complete

    def start_download_thread(self, out_folder: str):
        if self.download_status == DownloadStatus.pending:
            self.download_button.disabled = True
            self.download_button.text = "downloading"
            self.download_button.disabled_color = "red"
            Thread1 = threading.Thread(target=self.download, args=(out_folder,))
            Thread1.start()

    def delete(self):
        if self.download_status == DownloadStatus.pending or self.download_status == DownloadStatus.complete:
            self.delete_status = 1
            self.box_card.clear_widgets()
