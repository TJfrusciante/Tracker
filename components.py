import flet as ft
import datetime

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
        self.functions=Functions(layout,self)
        #COMPONETS THAT WILL BE USED IN THE LAYOUT FILE
        #SEPARATED PARTS STORED IN VARIABLES FOR BETTER ACESS TO DATA
        
        #COMPONENTS USED IN MONEY
        self.description_money=ft.TextField(
                    text_style=black,
                    value='',
                    label='Descrição da transação',
                    label_style=teal,
                    on_change=self.functions.set_value_money,
                    on_submit=self.functions.limpar_value_text_box_money
                )
        
        self.value_money=ft.TextField(
                    text_style=black,
                    value='',
                    label='Valor da transação',
                    label_style=teal,
                    width=100,
                    on_change=self.functions.set_value_money_float,
                    on_submit=self.functions.limpar_value_text_box_money
                )
        
        self.popup_money=ft.PopupMenuButton(
                    icon=ft.icons.TOPIC_OUTLINED,
                    tooltip='Selecionar seção',
                    col={'xs':0.5,'xl':2},
                    items=[
                    ft.PopupMenuItem(text='Cartão',checked=False,on_click=self.functions.check),
                    ft.PopupMenuItem(text='Gasolina',checked=False,on_click=self.functions.check),
                    ft.PopupMenuItem(text='Apartamento',checked=False,on_click=self.functions.check),
                    ft.PopupMenuItem(text='Internet',checked=False,on_click=self.functions.check),
                    ft.PopupMenuItem(text='Diversos',checked=False,on_click=self.functions.check),
                    ft.PopupMenuItem(text='Picpay',checked=False,on_click=self.functions.check),
                    ft.PopupMenuItem(text='Ações',checked=False,on_click=self.functions.check),
                    ft.PopupMenuItem(text='FIIs',checked=False,on_click=self.functions.check),
                    ft.PopupMenuItem(text='Salário',checked=False,on_click=self.functions.check),
                    ft.PopupMenuItem(text='Anderson',checked=False,on_click=self.functions.check),
                    ft.PopupMenuItem(text='Paula',checked=False,on_click=self.functions.check),
                    ft.PopupMenuItem(text='Mãe / Michelle',checked=False,on_click=self.functions.check),
                    ft.PopupMenuItem(text='Outros',checked=False,on_click=self.functions.check),
                    ft.PopupMenuItem(text='Hora extra',checked=False,on_click=self.functions.check)
                    ],   
                )
        
        self.tabs_money = ft.Tabs(
            divider_color='teal',
            selected_index=2,
            unselected_label_color=ft.colors.BLACK,
            label_color=ft.colors.TEAL,
            indicator_color=ft.colors.BLUE,
            tab_alignment=ft.TabAlignment.CENTER,
            on_change=self.functions.tabs_changed_money,
            tabs=[
                ft.Tab(text="Entradas"), 
                ft.Tab(text="Saídas"), 
                ft.Tab(text="Todos")
            ],
        )

        

        self.row_money_insert= ft.Row(
            controls=[
                self.description_money
                ,
                self.value_money
                ,
                self.popup_money
                ,
                ft.IconButton(
                    icon=ft.icons.CALENDAR_MONTH_OUTLINED,
                    on_click=lambda _: self.calendario.pick_date(),
                    tooltip="Selecionar data",
                    icon_color=cor_teal
                ),
                ft.IconButton(icon=ft.icons.ADD,
                              icon_color=ft.colors.TEAL,
                              col=1,
                              tooltip='Adicionar transação',
                              on_click=self.functions.limpar_value_text_box_money),
                ft.IconButton(icon=ft.icons.DELETE,
                              icon_color=ft.colors.RED,
                              col=1,
                              tooltip='Deletar transação',
                              on_click=self.functions.del_transaction)    
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER
            )
        
        self.column_money= ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            col=6,
            controls=[
                self.row_money_insert,
                self.tabs_money,
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START
        )


        #COMPONENTS USED IN TASKS
        self.data=ft.IconButton(
                    icon=ft.icons.CALENDAR_MONTH_OUTLINED,
                    icon_color=cor_teal,
                    on_click=lambda _: self.calendario.pick_date(),
                    tooltip="Escolha uma data"
                )
        
        self.description=ft.TextField(
                    width=300,
                    value='',
                    label='Descrição da tarefa',
                    label_style=teal,
                    on_change=self.functions.set_value,
                    on_submit=self.functions.limpar_value_text_box,
                    text_style=black
                )

        #COMPONENTS USED IN TRANSACTIONS

        #CALENDAR TO RETRIEVE THE DATE
        self.calendario=ft.DatePicker(
            first_date=datetime.datetime(year=2024,month=1,day=1),
            last_date=datetime.datetime(year=2035,month=1,day=1),
            on_dismiss=lambda _: print(f"A ultima data selecionada é: {str(self.calendario.value)[0:10]}"),
            help_text="Selecione a data",
            cancel_text="Cancelar",
            confirm_text="Confirmar"
        )

        #EDIT ALERT DIALOAG ELEMENTS WHICH I HAVE TO RETRIEVE DATA FROM
        self.text_field_edit=ft.TextField(label="Digite a nova descrição aqui",
                                        col=2,
                                        value='',
                                        on_change=self.functions.set_value,
                                        on_submit=self.functions.save_task_edit,
                                        text_style=black,
                                        label_style=ft.TextStyle(color=cor_black),
                                    )
        self.calendario_alert_icon=ft.TextButton(
            text='Nova data',
            icon=ft.icons.CALENDAR_MONTH_OUTLINED,
            icon_color=cor_black,
            style=ft.ButtonStyle(color={
                                        ft.MaterialState.DEFAULT: cor_black,
                                        ft.MaterialState.HOVERED: cor_amber
                                    }),
            col=1,
            tooltip="Selecionar data edição",
            on_click=lambda _: self.calendario.pick_date()
        )
        self.value_edit_money=ft.TextField(label="Digite o novo valor aqui",
                                           col=2,
                                            value='',
                                            on_change=self.functions.set_value,
                                            on_submit=self.functions.save_task_edit,
                                            text_style=black,
                                            label_style=ft.TextStyle(color=cor_black),
                                            )
        #DEFINING THE EDITING POPUPS
        self.edit_dialog_task = ft.AlertDialog(
            content=ft.Container(
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    height=300,
                    width=400,
                    controls=[
                        self.text_field_edit,
                        self.calendario_alert_icon,
                        ft.TextButton("Salvar",
                                    on_click=self.functions.save_task_edit,
                                    style=ft.ButtonStyle(color={
                                        ft.MaterialState.DEFAULT: cor_black,
                                        ft.MaterialState.HOVERED: cor_amber
                                    }),
                                    icon=ft.icons.SAVE_OUTLINED,
                                    icon_color=cor_black,
                                    ),

                        ft.TextButton("Cancelar",
                                    on_click=self.functions.close_dialog,
                                    style=ft.ButtonStyle(color={
                                        ft.MaterialState.DEFAULT: cor_black,
                                        ft.MaterialState.HOVERED: cor_amber
                                    }),
                                    icon=ft.icons.CANCEL_OUTLINED,
                                    icon_color=cor_black)
                    ]
                ),
                bgcolor=cor_teal,
                padding=20,
                border_radius=5
            ),
            actions=[
            ],
            visible=False,
        )
        self.edit_dialog_money = ft.AlertDialog(
            content=ft.Container(
                content=ft.Column(
                    col=10,
                    tight=True,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    
                    height=300,
                    width=400,
                    controls=[
                        self.text_field_edit,
                        self.value_edit_money,
                        self.calendario_alert_icon,
                        ft.TextButton("Salvar",
                                      col=1,
                                    on_click=self.functions.save_task_edit_money,
                                    style=ft.ButtonStyle(color={
                                        ft.MaterialState.DEFAULT: cor_black,
                                        ft.MaterialState.HOVERED: cor_amber
                                    }),
                                    icon=ft.icons.SAVE_OUTLINED,
                                    icon_color=cor_black,
                                    ),

                        ft.TextButton("Cancelar",
                                    col=1,
                                    on_click=self.functions.close_dialog_money,
                                    style=ft.ButtonStyle(color={
                                        ft.MaterialState.DEFAULT: cor_black,
                                        ft.MaterialState.HOVERED: cor_amber
                                    }),
                                    icon=ft.icons.CANCEL_OUTLINED,
                                    icon_color=cor_black)
                    ]
                ),
                bgcolor=cor_teal,
                padding=20,
                border_radius=5
            ),
            actions=[
            ],
            visible=False,
        )
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
                on_change=self.functions.tabs_changed
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
            on_change=self.functions.main_tabs_change
        )

        #ROWS
        self.row_tasks_insert=ft.Row(
            wrap=False,
            controls=[
                self.description,
                self.data,
                ft.IconButton(icon=ft.icons.ADD,icon_color=ft.colors.TEAL,col=1,on_click=self.functions.limpar_value_text_box),
                ft.IconButton(icon=ft.icons.DELETE,icon_color=ft.colors.RED,col=1,on_click=self.functions.del_tarefa)   
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
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            col=6,
            controls=[
                self.row_tasks_insert,
                self.tabs
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            
        )

        #CONTAINERS
        self.Container_money=ft.Container(
        col=6,
        content=self.column_money,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.colors.AMBER,ft.colors.YELLOW]
            ),
            padding=10
        )
        
        self.container_main=ft.Container(
            expand=True,
            col=6,
            content=self.column_tasks,
             gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.colors.AMBER,ft.colors.YELLOW]
                ),
                padding=10,
        )
        #LAYOUT THAT'S ADDED ON THE SCREEN
        self.layout=ft.Column(
        
        expand=True,
        controls=[
            self.container_main,
            self.row_change_main,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
        
        self.functions=Functions(layout,self)

