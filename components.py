import flet as ft

from Tracker.functions import Functions

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

class Components():
    def __init__(self,layout) -> None:
        #INSTANCES OF OTHER CLASSES
        self.functions=Functions(layout)

        #COMPONETS THAT WILL BE USED IN THE LAYOUT FILE
        #SEPARATED PARTS STORED IN VARIABLES FOR BETTER ACESS TO DATA

        #Tabs
        self.tabs = ft.Tabs(
                divider_color='teal',
                selected_index=0,
                unselected_label_color=ft.colors.BLACK,
                label_color=ft.colors.TEAL,
                indicator_color=ft.colors.BLUE,
                tab_alignment=ft.TabAlignment.CENTER,
                tabs=[
                    ft.Tab(text="Todos"), 
                    ft.Tab(text="Em andamento"), 
                    ft.Tab(text="Finalizados")
                ],
            )
        
        #NAVIGATION BAR
        self.nav_bar=ft.NavigationBar(
            adaptive=True,
            destinations=[
                ft.NavigationDestination(icon=ft.icons.MONETIZATION_ON_ROUNDED,
                                        tooltip="Clique para visualizar suas transações",
                                        label="Transações"),
                ft.NavigationDestination(icon=ft.icons.BOOK_ROUNDED,
                                        tooltip="Clique para visualizar suas tarefas",
                                        selected_icon=ft.icons.BOOK_OUTLINED, label="Tarefas")
            ]
            ,
            selected_index=1,
            label_behavior=ft.NavigationBarLabelBehavior.ONLY_SHOW_SELECTED,
            indicator_color=ft.colors.AMBER,
            bgcolor=ft.colors.TEAL,
            shadow_color=ft.colors.BLACK,
        )

        #ROWS
        self.row_tasks_insert=ft.Row(
            wrap=False,
            controls=[
                ft.IconButton(icon=ft.icons.ADD,icon_color=ft.colors.TEAL,col=1,on_click=self.functions.teste),
                ft.IconButton(icon=ft.icons.DELETE,icon_color=ft.colors.RED,col=1,on_click=self.functions.teste)   
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        self.row_change_main=ft.Container(
            content=self.nav_bar,
            bgcolor=cor_white,
             gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.colors.AMBER,ft.colors.YELLOW]
                ),
        )
        
        #COLUMNS
        self.column_tasks=ft.Column(
            expand=True,
            col=6,
            controls=[
                self.row_tasks_insert,
                self.tabs
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )

        self.container_main=ft.Container(
            expand=True,
            content=self.column_tasks,
             gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.colors.AMBER,ft.colors.YELLOW]
                ),
        )
        
        self.layout=ft.Column(
        
        expand=True,
        controls=[
            self.container_main,
            self.row_change_main,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

