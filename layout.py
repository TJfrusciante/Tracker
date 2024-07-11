import flet as ft

from Tracker.functions import Functions
from Tracker.components import Components
from Tracker.flet_colors import Flet_colors

class Layout():
    def __init__(self, page) -> None:
        self.colors=Flet_colors()

        self.page=page
        self.page.title='Tracker 1.0'
        self.page.bgcolor=self.colors.cor_black
        self.page.padding= ft.padding.all(10)
        self.page.theme=ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=self.colors.cor_black,#primários, exemplo: cancelar/confirmar/ok
                on_primary=self.colors.cor_white,#cor dentro dos primarys, exemplo: número dentro da data selecionada no DatePicker
                on_surface=self.colors.cor_black,#cor de coisas na superficie, exemplo: datas no DatePicker
                surface=self.colors.cor_amber,#cor das superficies, exemplo: cor de fundo do DatePicker
                surface_tint=self.colors.cor_green,#cor de alertDialog outerborder
                on_surface_variant=self.colors.cor_black,#cor de checkBox box border
                
                )
            )
        
        #INTANCES OF OTHER CLASSES
        self.components=Components(self)
        self.edit_data=''
        self.task = ''
        self.view = 'all'

        #ADDING THINGS TO THE OVERLAY
        self.page.overlay.append(self.components.edit_dialog_task)
        self.page.overlay.append(self.components.edit_dialog_money)
        self.page.overlay.append(self.components.calendario)
        self.page.overlay.append(self.components.edit_categories)
        self.page.overlay.append(self.components.chart_creating_popup)
        self.page.overlay.append(self.components.chart_image_popup)

        #ADDING THINGS TO THE PAGE
        self.page.add(self.components.layout)
        self.page.on_keyboard_event = self.components.functions.handle_key_event
        self.update_page()

    def add_to_page(self, item_to_add):
        self.page.add(item_to_add)

    def update_page(self):
        self.page.update()