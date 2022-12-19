from kivymd.uix.list import MDList

from UI_Widget.yt_item import YTItem, DownloadStatus
import UI_Widget.Global_Data as gd


class YTList(MDList):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list: list[YTItem] = []

    def add_item(self, item: YTItem):
        widget = item.build_widget()
        self.list.append(item)
        self.add_widget(widget)

    def download_all(self):
        for item in self.list:
            if item.delete_status == 1:
                self.list.remove(item)
        for item in self.list:
            item.start_download_thread(gd.download_dir)

    def delete_complete(self):
        for item in self.list:
            if item.download_status == DownloadStatus.complete:
                item.delete()
        for item in self.list:
            if item.download_status == DownloadStatus.complete:
                self.list.remove(item)
