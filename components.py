from textwrap import wrap
from turtle import bgcolor
import flet as ft
import datetime

from Tracker.functions import Functions

#Cores de texto
black=ft.TextStyle(color=ft.colors.BLACK, weight=ft.FontWeight.BOLD)
green=ft.TextStyle(color=ft.colors.GREEN, weight=ft.FontWeight.BOLD)
red=ft.TextStyle(color=ft.colors.RED, weight=ft.FontWeight.BOLD)
teal=ft.TextStyle(color=ft.colors.TEAL, weight=ft.FontWeight.W_500)
amber=ft.TextStyle(color=ft.colors.AMBER, weight=ft.FontWeight.W_500)
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
        
        #ALERT DIALOG TO SELECT THE PERIOD OF TIME WHICH THE MONEY TRANSACTIONS WILL BE CONVERTED INTO CHARTS
        self.months=['01- Janeiro', '02- Fevereiro', '03- Março', '04- Abril', '05- Maio', '06- Junho', '07- Julho', '08- Agosto', 
                     '09- Setembro', '10- Outubro', '11- Novembro', '12- Dezembro']
        self.month_picker=ft.Dropdown(
                    width=300,
                    label='Mês',
                    hint_text='Escolha o mês',
                    text_style=amber,
                    icon=ft.icons.DATE_RANGE,
                    tooltip='Selecionar mês',
                    col={'xs':0.5,'xl':2},
                    options=[
                      ft.dropdown.Option(text=month) for month in self.months  
                    ]  ,   
                )
        
        self.year_picker=ft.Dropdown(
                    width=150,
                    label='Ano',
                    hint_text='Escolha o ano',
                    text_style=amber,
                    tooltip='Selecionar ano',
                    col={'xs':0.5,'xl':2},
                    options=[
                        ft.dropdown.Option(text=str(item)) for item in range (2024,2050)  
                    ],   
                )

        self.chart_creating_popup=ft.AlertDialog(
            content=ft.Container(
                expand=True,
                content=ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=25,
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    height=400,
                    width=500,
                    controls=[
                        ft.Row(
                            controls=[
                            self.month_picker,
                            self.year_picker]
                        ),
                        
                        ft.Row(     
                                controls=[
                                ft.TextButton("Gerar gráficos",
                                on_click=self.functions.create_chart,
                                style=ft.ButtonStyle(color={
                                    ft.MaterialState.DEFAULT: cor_black,
                                    ft.MaterialState.HOVERED: cor_amber
                                }),
                                icon=ft.icons.ADD,
                                icon_color=cor_black,
                                ),
                                ]),
                
                        ft.TextButton("Cancelar",
                                    on_click=self.functions.close_charts_creation,
                                    style=ft.ButtonStyle(color={
                                        ft.MaterialState.DEFAULT: cor_black,
                                        ft.MaterialState.HOVERED: cor_amber
                                    }),
                                    icon=ft.icons.CANCEL_OUTLINED,
                                    icon_color=cor_black),
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

        self.chart_image_popup=ft.AlertDialog(
            content=ft.Row(
                expand=True,
                controls=[
                    ft.Image()
                ],
            ),
            actions=[
            ],
            visible=False,
        )
        
        
        #SCREEN TO EDIT THE CATEGORIES IN MONEY TRANSACTIONS
        self.text_field_edit_category=ft.TextField(
            value='',
            label="Digite a nova categoria aqui",
            on_change=self.functions.set_value,
            on_submit=self.functions.add_category,
            text_style=black,
            label_style=ft.TextStyle(color=cor_black),
        )
        self.existent_categories=ft.Column(
            controls=[],
            )

        self.edit_categories= ft.AlertDialog(
            content=ft.Container(
                expand=True,
                content=ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=25,
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    height=400,
                    width=500,
                    controls=[
                        self.text_field_edit_category,
                        ft.Row(col=2,
                                controls=[
                                    ft.TextButton("Adicionar categoria",
                                    on_click=self.functions.add_category,
                                    style=ft.ButtonStyle(color={
                                        ft.MaterialState.DEFAULT: cor_black,
                                        ft.MaterialState.HOVERED: cor_amber
                                    }),
                                    icon=ft.icons.ADD,
                                    icon_color=cor_black,
                                    ),
                                    ft.TextButton("Remover categoria",
                                    on_click=self.functions.del_category,
                                    style=ft.ButtonStyle(color={
                                        ft.MaterialState.DEFAULT: cor_black,
                                        ft.MaterialState.HOVERED: cor_amber
                                    }),
                                    icon=ft.icons.REMOVE,
                                    icon_color=cor_black,
                                    ),
                                    ]),
                    
                        ft.TextButton("Cancelar",
                                    on_click=self.functions.close_edit_categories,
                                    style=ft.ButtonStyle(color={
                                        ft.MaterialState.DEFAULT: cor_black,
                                        ft.MaterialState.HOVERED: cor_amber
                                    }),
                                    icon=ft.icons.CANCEL_OUTLINED,
                                    icon_color=cor_black),
                        self.existent_categories
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
                    tooltip='Selecionar categoria',
                    col={'xs':0.5,'xl':2},
                    items=[
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
                    icon_color=cor_black
                ),
                ft.IconButton(icon=ft.icons.ADD,
                              icon_color=cor_teal,
                              col=1,
                              tooltip='Adicionar transação',
                              on_click=self.functions.limpar_value_text_box_money),
                ft.IconButton(icon=ft.icons.DELETE,
                              icon_color=cor_red,
                              col=1,
                              tooltip='Deletar transação',
                              on_click=self.functions.del_transaction),

                ft.IconButton(icon=ft.icons.EDIT_NOTE,
                              icon_color=cor_black,
                              col=1,
                              tooltip='Editar categorias',
                              on_click=self.functions.open_edit_categories),

                ft.IconButton(icon=ft.icons.ADD_CHART,
                              icon_color=cor_teal,
                              col=1,
                              tooltip='Gerar gráficos',
                              on_click=self.functions.open_charts_creation) 
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER
            )
        
        self.tabs_money = ft.Tabs(
            divider_color='teal',
            selected_index=2,
            unselected_label_color=cor_black,
            label_color=cor_teal,
            indicator_color=cor_blue,
            tab_alignment=ft.TabAlignment.CENTER,
            on_change=self.functions.tabs_changed_money,
            tabs=[
                ft.Tab(text="Entradas"), 
                ft.Tab(text="Saídas"), 
                ft.Tab(text="Todos")
            ],
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
        self.text_field_edit_task=ft.TextField(label="Digite a nova descrição",
                                        col=2,
                                        value='',
                                        on_change=self.functions.set_value,
                                        on_submit=self.functions.save_task_edit,
                                        text_style=black,
                                        label_style=ft.TextStyle(color=cor_black),
                                    )
        self.text_field_edit=ft.TextField(label="Digite a nova descrição",
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
        self.value_edit_money=ft.TextField(
                                            width=195,
                                            label="Novo valor",
                                            col=1,
                                            value='',
                                            on_change=self.functions.set_value,
                                            on_submit=self.functions.save_task_edit,
                                            text_style=black,
                                            label_style=ft.TextStyle(color=cor_black),
                                            )
        self.category_edit_money= ft.TextField(
                                            width=195,
                                            label="Nova categoria",
                                            col=1,
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
                        self.text_field_edit_task,
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
                        ft.Row(
                            col=2,
                            controls=[
                                self.value_edit_money,
                                self.category_edit_money]
                        ),
                        
                        self.calendario_alert_icon,
                        ft.Row(
                            controls=[ft.TextButton("Salvar",
                                      col=1,
                                    on_click=self.functions.save_transaction_edit_money,
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
                                    icon_color=cor_black)])
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
                unselected_label_color=cor_black,
                label_color=cor_teal,
                indicator_color=cor_blue,
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
            indicator_color=cor_amber,
            bgcolor=cor_teal,
            shadow_color=cor_black,
            on_change=self.functions.main_tabs_change
        )

        #ROWS
        self.row_tasks_insert=ft.Row(
            wrap=False,
            controls=[
                self.description,
                self.data,
                ft.IconButton(icon=ft.icons.ADD,icon_color=cor_teal,col=1,on_click=self.functions.limpar_value_text_box),
                ft.IconButton(icon=ft.icons.DELETE,icon_color=cor_red,col=1,on_click=self.functions.del_tarefa)   
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        self.row_change_main=ft.Container(
            content=self.nav_bar,
            bgcolor=cor_white,
             gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[cor_amber,ft.colors.YELLOW]
                ),
        )
        
        #COLUMNS
        self.column_tasks=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            controls=[
                self.row_tasks_insert,
                self.tabs
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )
        #VARIABLE TO STORE THE HEADER OF THE APP SO IT CAN STAY FIXED JUST AS THE FOOTER
        self.header=ft.Container(
        content=self.column_tasks,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[cor_amber,ft.colors.YELLOW]
            ),
            padding=10
        )
        #VARIABLE TO STORE A BODY COMPONENT, WHICH WILL BE SCROLLABE
        self.body_container=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            controls=[
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )
        #CONTAINERS
        self.Container_money=ft.Container(
        expand=True,
        content=self.column_money,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[cor_amber,ft.colors.YELLOW]
            ),
            padding=10
        )
        
        self.container_main=ft.Container(
            expand=True,
            content=self.body_container,
             gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.colors.YELLOW,cor_amber]
                ),
                padding=10,
        )
        #LAYOUT THAT'S ADDED ON THE SCREEN
        self.layout=ft.Column(
        expand=True,
        controls=[
            self.header,
            self.container_main,
            self.row_change_main,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
        
        self.functions=Functions(layout,self)

