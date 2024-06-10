import flet as ft

from Tracker.functions import Functions
from Tracker.components import Components


#Cores de texto
black=ft.TextStyle(color=ft.colors.BLACK, weight=ft.FontWeight.BOLD)
green=ft.TextStyle(color=ft.colors.GREEN, weight=ft.FontWeight.BOLD)
red=ft.TextStyle(color=ft.colors.RED, weight=ft.FontWeight.BOLD)
teal=ft.TextStyle(color=ft.colors.TEAL, weight=ft.FontWeight.W_500)
invisible_label_style = ft.TextStyle(color=ft.colors.TRANSPARENT)
#Cores
cor_black=ft.colors.BLACK
cor_teal=ft.colors.TEAL
cor_amber=ft.colors.AMBER
cor_red=ft.colors.RED
cor_green=ft.colors.GREEN
cor_blue=ft.colors.BLUE
cor_white=ft.colors.WHITE
class Layout():
    def __init__(self, page) -> None:
        self.page=page
        self.page.title='Tracker 1.0'
        self.page.bgcolor=cor_black
        self.page.theme=ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=cor_black,#primários, exemplo: cancelar/confirmar/ok
                on_primary=cor_white,#cor dentro dos primarys, exemplo: número dentro da data selecionada no DatePicker
                on_surface=cor_black,#cor de coisas na superficie, exemplo: datas no DatePicker
                surface=cor_amber,#cor das superficies, exemplo: cor de fundo do DatePicker
                surface_tint=cor_green,#cor de alertDialog outerborder
                on_surface_variant=cor_black,#cor de checkBox box border
                
                )
            )
        
        #INTANCES OF OTHER CLASSES
        self.components=Components(self)

        self.edit_data=''
        self.task = ''
        self.view = 'all'

        self.page.add(self.components.layout)
        self.update_page()

    def add_to_page(self, item_to_add):
        self.page.add(item_to_add)

    def update_page(self):
        self.page.update()