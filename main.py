import flet as ft
import datetime

from Tracker.layout  import Layout

class Tracker():
    def __init__(self, page: ft.Page) -> None:
        Layout(page)

if __name__=='__main__':
    ft.app(target=Tracker, assets_dir='assets')
    
        