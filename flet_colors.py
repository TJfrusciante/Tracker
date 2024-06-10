import flet as ft

class Flet_colors():
    def __init__(self) -> None:
        #Cores de texto
        self.text_black= ft.TextStyle(color=ft.colors.BLACK, weight=ft.FontWeight.BOLD)
        self.text_green=ft.TextStyle(color=ft.colors.GREEN, weight=ft.FontWeight.BOLD)
        self.text_red=ft.TextStyle(color=ft.colors.RED, weight=ft.FontWeight.BOLD)
        self.text_teal=ft.TextStyle(color=ft.colors.TEAL, weight=ft.FontWeight.W_500)
        self.text_invisible_label_style = ft.TextStyle(color=ft.colors.TRANSPARENT)
        #Cores
        self.cor_black=ft.colors.BLACK
        self.cor_teal=ft.colors.TEAL
        self.cor_amber=ft.colors.AMBER
        self.cor_red=ft.colors.RED
        self.cor_green=ft.colors.GREEN
        self.cor_blue=ft.colors.BLUE
        self.cor_white=ft.colors.WHITE
        self.cor_orange=ft.colors.ORANGE
