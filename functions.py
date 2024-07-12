from multiprocessing import Value
from tkinter.font import BOLD
from turtle import bgcolor
import flet as ft
import matplotlib
import matplotlib.lines
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import io
from PIL import Image

from Tracker.database import Database
from Tracker.flet_colors import Flet_colors

from functools import wraps


class Functions():

    def __init__(self,layout,components) -> None:
        #INSTANTIATING LAYOUT AND COMPONENTS CLASS USING THE SELF PARAMETER OF EXISTENT INSTANCES
        self.layout=layout
        self.components=components
        #INTANCES
        self.data_base=Database()
        self.colors=Flet_colors()
        #INITIATING VARIABLES
        self.components.edit_data=''
        self.components.edit_data_money=''
        self.task = ''
        
        self.view = 'all'
        
        self.atualizar_money()
        self.atualizar_tarefas()
        
        
    @staticmethod
    def update_tasks_db(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return  func(self, *args, **kwargs), self.atualizar_tarefas()
        return wrapper
    
    @staticmethod
    def update_money_db(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs),self.atualizar_money()
        return wrapper
    
    def check(self,e):#check the category of money transaction to add a new transaction
        e.control.checked= not e.control.checked
        self.text_money=e.control.text
        e.control.update()
    

    #CHARTS CREATION METHODS
    def open_charts_creation(self, e):
        self.components.chart_creating_popup.open = True
        self.components.chart_creating_popup.visible=True
        self.layout.page.update()

    def close_charts_creation(self, e):
        self.components.chart_creating_popup.open = False
        self.layout.page.update()

    def sum_values_for_the_chart(self):
        self.category_value_date=self.data_base.manipular_db('SELECT category, value, date FROM money')
        
        self.dict_categories_values=dict()
    
        self.date_to_chart=f'{self.components.month_picker.value.split('-')[0]}/{self.components.year_picker.value}'
        
        for x in self.category_value_date:
            self.dict_categories_values[x[0]]=[]#initializing dict keys for each category

        for x in self.category_value_date:
            print(x[2][3:],'data da lista')
            if x[2][3:]==self.date_to_chart:
                self.dict_categories_values[x[0]].append(x[1])#appending values to it's corresponding category key
            else:
                print(f'{x} esta data não esta no intervalo selecinado')
        self.categorias_list=[]
        self.valores_list=[]
        for key in self.dict_categories_values.keys():
            self.categorias_list.append(key)
            self.valores_list.append(sum(self.dict_categories_values[key]))
            # print(f'O resultado na categoria {key} em {self.date_to_chart} foi de: {sum(self.dict_categories_values[key])} reais.')
        print(self.categorias_list,'categorias')
        print(self.valores_list,'valores')
        
    def create_chart(self, e):
        self.sum_values_for_the_chart()
        
        #SETTING THE CHART STYLES
        #['Solarize_Light2', '_classic_test_patch', '_mpl-gallery', '_mpl-gallery-nogrid', 'bmh', 'classic', 'dark_background', 
        #'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn-v0_8', 'seaborn-v0_8-bright', 'seaborn-v0_8-colorblind',
        #'seaborn-v0_8-dark', 'seaborn-v0_8-dark-palette', 'seaborn-v0_8-darkgrid', 
        # 'seaborn-v0_8-deep', 'seaborn-v0_8-muted', 'seaborn-v0_8-notebook', 'seaborn-v0_8-paper', 'seaborn-v0_8-pastel', 
        # 'seaborn-v0_8-poster', 'seaborn-v0_8-talk', 'seaborn-v0_8-ticks', 'seaborn-v0_8-white', 'seaborn-v0_8-whitegrid', 'tableau-colorblind10']
        plt.style.use('fivethirtyeight')
        my_colors = ['#FFBF00','#008000','#FF0000','#A020F0','#ffa500','#e94196']
        #CREATING BAR CHART
        fig, ax = plt.subplots(figsize=(10, 6))
    
        bars = ax.bar(
            self.categorias_list,
            self.valores_list,
            width=0.4
        )
        
        legend_handles = []
        #SETTING EACH BAR
        for index in range(len(bars)):
            bars[index].set_edgecolor('black')
            bars[index].set_linewidth(1.2)
            legend_handle = matplotlib.lines.Line2D([0], [0], color=my_colors[index], lw=4, label=self.categorias_list[index])
            legend_handles.append(legend_handle)
            bars[index].set_color(my_colors[index])
        
        #ADDING GRID
        ax.grid(True, linestyle='--', alpha=0.7,color='#000000')
        
        #LABELS AND TITLE
        ax.set_xlabel('Categorias', fontsize=14, fontweight='bold',color='#000000')
        ax.set_ylabel('Valores (Reais)', fontsize=14, fontweight='bold',color='#000000')
        ax.set_title(f'Resumo do mês {self.date_to_chart}', fontsize=16, fontweight='bold', pad=20)
        
        #ROTATING X-AXIS LABELS 
        plt.xticks(rotation=45, ha='right')
        
        #ADDING EACH CATEGORY VALUE IN EACH BAR
        for bar in bars:
            yval = bar.get_height()
            if yval > 0:
                color = '#008000'
            else:
                color = '#FF0000'
            ax.text(bar.get_x() + bar.get_width()/2, yval + 10, f'${yval}', ha='center', va='bottom', fontsize=12, color=color)
        
        #ADD A LEGEND TO EACH CATEGORY
        ax.legend(handles=legend_handles, loc='upper left', frameon=True)
        #ADDING BACKGROUND COLOR
        fig.patch.set_facecolor('lightgrey')

        #MAKING SURE THAT THE Y-AXIS IS ALWAYS A BIT HIGHER THAN THE HIGHEST VALUE, SO THE VALUE REPRESENTATION WON'T BE CUT OFF
        max_value = max(self.valores_list)
        min_value = min(self.valores_list)
        ax.set_ylim(min_value + min_value * 0.1, max_value + max_value * 0.1)  # Adding 10% buffer to the top
        
        #SHOWING CHART
        plt.tight_layout()
        plt.show()

    #CATEGORY EDITING SCREEN METHODS
    def update_existent_categories(self):
        self.components.existent_categories.controls=[ft.Text(value='Categorias atuais:',color=self.colors.cor_black, weight=ft.FontWeight.BOLD)]
        for category in self.data_base.categories:
            self.components.existent_categories.controls.append(ft.Text(value=f' {category[0]}',color=self.colors.cor_amber, weight=ft.FontWeight.BOLD))
        
    def open_edit_categories(self, e):
        self.update_categories()
        self.components.edit_categories.open = True
        self.components.edit_categories.visible=True
        self.update_existent_categories()
        self.layout.page.update()

    def close_edit_categories(self, e):
        self.components.edit_categories.open = False
        self.layout.page.update()

    def add_category(self, e):
        self.data_base.manipular_db(command='INSERT INTO categories (category) SELECT ? WHERE NOT EXISTS (SELECT 1 FROM categories WHERE category = ?)',
        parametros=[self.components.text_field_edit_category.value, self.components.text_field_edit_category.value])
        self.components.text_field_edit_category.value=''
        self.close_edit_categories(self.components.edit_categories)
        self.update_categories()
        self.layout.page.update()
    
    def del_category(self, e):
        self.data_base.manipular_db(command='DELETE FROM categories WHERE category = ?',parametros=[self.components.text_field_edit_category.value])
        self.components.text_field_edit_category.value=''
        self.close_edit_categories(self.components.edit_categories)
        self.update_categories()
        self.layout.page.update()
        
    def update_categories(self):
        self.data_base.categories=self.data_base.manipular_db('SELECT category FROM categories')
        categories_list=[]
        for item in self.data_base.categories:
            categorie=ft.PopupMenuItem(
                text=item[0],
                checked=False,
                on_click=self.check,
            )
            categories_list.append(categorie)

        self.components.popup_money.items= categories_list

    #ALERT DIALOAG METHODS
    def open_dialog(self, e):
        self.components.edit_dialog_task.open = True
        self.components.edit_dialog_task.visible=True
        self.layout.page.update()
        self.components.edit_data=e.control.data
        
    def close_dialog(self, e):
        self.components.edit_dialog_task.open= False
        self.layout.page.update()

    def open_dialog_money(self, e):
        self.components.edit_dialog_money.open = True
        self.components.edit_dialog_money.visible=True
        self.layout.page.update()
        self.components.edit_data_money=e.control.data

    def close_dialog_money(self, e):
        self.components.edit_dialog_money.open= False
        self.layout.page.update()

    #EVENT HANDLER WHEN KEYBOARD IS USED
    def handle_key_event(self, event):
        # print(event.key,'tecla') #Para saber como chamar a tecla pressionada
        if event.key == "Escape":
            self.close_dialog(event) 

        elif event.key =="Tab" and event.shift:
            self.components.nav_bar.selected_index = 1 if self.components.header.content == self.components.Container_money else 0
            self.main_tabs_change((self.components.nav_bar))
            
        elif event.key =="Delete":
            if self.components.nav_bar.selected_index==0:
                self.del_transaction(self.components.row_money_insert.controls[5])
            else:
                self.del_tarefa(self.components.row_tasks_insert.controls[3])#chamando com o icone de delete só pra padronizar

        if event.key == "Numpad Add":
            if self.components.nav_bar.selected_index==0:
                self.layout.page.update()
                self.layout.components.functions.limpar_value_text_box_money(self.components.row_money_insert.controls[4])
            else:
                self.add_tarefa(self.components.row_tasks_insert.controls[2])#chamando com o icone de delete só pra padronizar

    #MAIN TABS CHANGE METHOD
    def main_tabs_change(self,e):
        try:
            if self.components.nav_bar.selected_index==0:
                self.view='all_money'
        
                self.components.header.content=self.components.Container_money
                self.atualizar_money()
                self.update_categories()
    
            else:
        
                self.components.header.content=self.components.column_tasks
                self.view='all'
                self.atualizar_tarefas()
            
        except:
            if self.components.nav_bar.selected_index==0:
                self.view='all_money'
                self.atualizar_money()
                self.update_categories()
    
            else:
        
                self.components.header.content=self.components.column_tasks
                self.view='all'
                self.atualizar_tarefas()

        self.components.nav_bar.update()
        self.components.layout.update()

    #METHOD THAT AFFECTS THE MONEY
    def money_containers(self):
        money_rows_containers=[]
        if self.data_base.transactions!=[]:
            for transaction in self.data_base.transactions:
                row_money= ft.Row(
                            width=5000,#TO MAKE SURE THE ROW IS AS LARGE AS THE SCREEN CAN BE, I COULDN'T FIND ANOTHER TO DO THIS, WHEN I SET EXPAND TO TRUE THE HEIGHT WAS AFFECTED AS WELL
                            tight=True,
                            scroll=ft.ScrollMode.AUTO ,
                            spacing=5,
                            controls=[
                                ft.Checkbox(
                                    adaptive=True,
                                    check_color=self.colors.cor_black,
                                    hover_color=self.colors.cor_teal,
                                    active_color=self.colors.cor_orange,
                                    focus_color=self.colors.cor_black,
                                    label=f"{transaction[0]}, {transaction[2]} reais,",
                                    label_style=self.colors.text_green if transaction[2]>0 else self.colors.text_red,
                                    label_position=ft.LabelPosition.RIGHT,
                                    tooltip="Selecionar lançamento",
                                    on_change=self.checked_money,
                                    value=True if transaction[3]=='ok' else False
                                ),
                                ft.Text(
                                    weight=ft.FontWeight.BOLD,
                                    color=self.colors.cor_green if transaction[2]>0 else self.colors.cor_red,
                                    value=f"lançamento dia: {transaction[1]}, Categoria {transaction[4]}."
                                ),
                                ft.IconButton(
                                    icon=ft.icons.EDIT,
                                    icon_color=self.colors.cor_teal,
                                    on_click=self.open_dialog_money,
                                    data=transaction[0]
                                )
                                ]
                                )
                money_rows_containers.append(row_money) 
            return money_rows_containers
        else:
            return [ft.Row(
                controls=[
                    ft.Text(value='Não há transações nesta categoria!', color=self.colors.cor_black, style=self.colors.text_black)
                ]
            )]

    @update_money_db
    def checked_money(self, e):
        is_checked = e.control.value
        label = e.control.label
        label=label.split(',')[0]#se colocar "," na description, tem que tratar para excluir, pois buga o split
        
        if is_checked:
            self.data_base.manipular_db('UPDATE money SET selected = "ok" WHERE description = ?', parametros=[label])
        elif is_checked ==False :
            self.data_base.manipular_db('UPDATE money SET selected = "no" WHERE description = ?', parametros=[label])
            
        if self.view == 'all_money': #atualizando valores na lista de transações para atualiza-las quando terminar de excluir
            self.transactions = self.data_base.manipular_db('SELECT * FROM money')
        elif self.view=='positive':
            self.transactions = self.data_base.manipular_db('SELECT * FROM money WHERE value > 0')
        elif self.view=='negative':
            self.transactions = self.data_base.manipular_db('SELECT * FROM money WHERE value < 0')

    
    def atualizar_money(self):#METHOD TO UPDATE TRANSACTIONS
        self.data_base.manipular_db(command='DELETE FROM money WHERE description = ?', parametros=['t'])
        try:
            try:
                if self.components.body_container.controls[0]:
                    self.components.body_container.controls = []  
                    if self.view=='all_money' or self.view=="all":
                        self.data_base.transactions = self.data_base.manipular_db('SELECT * FROM money')
        
                    elif self.view=='positive':
                        self.data_base.transactions = self.data_base.manipular_db('SELECT * FROM money WHERE value > 0;')
        
                    elif self.view=='negative':
                        self.data_base.transactions = self.data_base.manipular_db('SELECT * FROM money WHERE value < 0;')
                     
    
            except:
                print('exception ao atualizar money 1')
            money_rows=self.money_containers()
            self.components.body_container.controls.extend(money_rows)
            self.components.body_container.update()   
            self.components.header.update()
            self.components.layout.update()
        except:
            print('exception ao atualizar money 2')

    @update_money_db
    def add_transaction(self,e):
        
        for menu_item in self.components.popup_money.items:
            if menu_item.checked==True:
                category=menu_item.text
        value_money=(self.components.value_money.data)
        value_money=value_money.replace(',','.')
        value_money=float(value_money)

        selected='no'
        description=self.set_value_money(self.components.row_money_insert)
        # category=self.text_money
        date=str(self.components.calendario.value)[0:10]
        data_separada=date.split('-')
        data=data_separada[2]+'/'+data_separada[1]+'/'+data_separada[0]

        if description:
            self.data_base.manipular_db(command='INSERT INTO money VALUES(?,?,?,?,?)', parametros=[description,data,value_money,selected,category])
        
    @update_money_db
    def del_transaction(self,e):#in te tasks money, the column that tells if the checkbox is selected is index number 3
        check_list=self.data_base.transactions
        for item in check_list:
            if item[3]=='ok':
                self.data_base.manipular_db(command='DELETE FROM money WHERE description = ?', parametros=[item[0]])

    @update_money_db
    def save_transaction_edit_money(self, e):
        new_transaction_name = self.components.text_field_edit.value

        if new_transaction_name != '':
            self.data_base.manipular_db('UPDATE money SET description = ? WHERE description = ?', parametros=[new_transaction_name, self.components.edit_data_money])
            if self.components.value_edit_money.value!='':#HAD TO TREAT THIS CAUSE THE '' VALUE CANNOT BE CONVERTED TO INT
                new_transaction_value= float((self.components.value_edit_money.value).replace(',','.'))
                self.data_base.manipular_db('UPDATE money SET value = ? WHERE description = ?', parametros=[new_transaction_value, new_transaction_name])
            if self.components.calendario.value !=None:
                new_money_date=str(self.components.calendario.value)[0:10]
                data_separada=new_money_date.split('-')
                new_money_date=data_separada[2]+'/'+data_separada[1]+'/'+data_separada[0]
                self.data_base.manipular_db('UPDATE money SET date = ? WHERE description = ?', parametros=[new_money_date, new_transaction_name])
            if self.components.category_edit_money.value!= '':
                self.data_base.manipular_db('UPDATE money SET category = ? WHERE description = ?', parametros=[self.components.category_edit_money.value, new_transaction_name])
            self.components.edit_data_money=new_transaction_name
        else:
            if self.components.value_edit_money.value!='':#HAD TO TREAT THIS CAUSE THE '' VALUE CANNOT BE CONVERTED TO INT
                new_transaction_value= float((self.components.value_edit_money.value).replace(',','.'))
                self.data_base.manipular_db('UPDATE money SET value = ? WHERE description = ?', parametros=[new_transaction_value, self.components.edit_data_money])
            if self.components.calendario.value !=None:
                new_money_date=str(self.components.calendario.value)[0:10]
                data_separada=new_money_date.split('-')
                new_money_date=data_separada[2]+'/'+data_separada[1]+'/'+data_separada[0]
                self.data_base.manipular_db('UPDATE money SET date = ? WHERE description = ?', parametros=[new_money_date, self.components.edit_data_money])
            if self.components.category_edit_money.value!= '':
                self.data_base.manipular_db('UPDATE money SET category = ? WHERE description = ?', parametros=[self.components.category_edit_money.value, self.components.edit_data_money])
        
        #RESETING ALL COMPONENTS VALUE SO WHEN YOU OPEN THE EDIT SCREEN AGAIN ALL FIELDS ARE EMPTY, WAITING FOR NEW INPUTS FROM THE USER
        self.components.text_field_edit.value=''
        self.components.value_edit_money.value=''
        self.components.category_edit_money.value=''
        self.components.calendario.value=None

        self.close_dialog_money(self.components.edit_dialog_money)

    def return_checkbox_for_del_money(self):
        return [ft.Checkbox(
                        adaptive=True,
                        check_color=self.colors.cor_black,
                        hover_color=self.colors.cor_teal,
                        active_color=self.colors.cor_orange,
                        label=transacao[0],
                        label_style=self.colors.text_black,# type: ignore
                        label_position=ft.LabelPosition.RIGHT,
                        on_change=self.checked,
                        value=True if transacao[3]=='ok' else False
                        ) for transacao in self.data_base.transactions]
    
    def limpar_value_text_box_money(self,e):
        try:
            self.add_transaction(e=e)
            self.components.description_money.value=''
            self.components.value_money.value=''
            self.components.row_money_insert.update()
        except:
            print('erro ao apagar valor text box money')


    def tabs_changed_money(self, e):
        self.data_base.update_variables()
        if e.control.selected_index == 0:
            self.view = 'positive'
        elif e.control.selected_index == 1:
            self.view = 'negative'
        elif e.control.selected_index == 2:
            self.view = 'all_money'

        self.atualizar_money()

    def set_value_money_float(self, e):#SETTING TRANSACTION VALUE
        try:
            valor=e.controls[0].value    
        except:
            valor=e.control.value        
        
        self.components.value_money.data=valor

        return(valor)
          
    def set_value_money(self, e):#SETTING TRANSACTION DESCRIPTION
        try:
            nome=e.controls[0].value    
        except:
            nome=e.control.value        
        return(nome)
    

    #METHOD THAT AFFECTS THE TASKS
    def atualizar_tarefas(self):#METHOD TO UPDATE TASKS
        try:
            try:
                if self.components.body_container.controls[0]:
                    self.components.body_container.controls.clear()  
                    if self.view=='all':
                        self.data_base.results = self.data_base.manipular_db('SELECT * FROM tasks')
                    elif self.view=='done':
                        self.data_base.results = self.data_base.manipular_db('SELECT * FROM tasks WHERE status = "done"')
                    elif self.view=='ongoing':
                        self.data_base.results = self.data_base.manipular_db('SELECT * FROM tasks WHERE status = "ongoing"')
            except:
                print('exception ao atualizar tarefas 1 ')
            task_rows = self.task_containers()
            self.components.body_container.controls.extend(task_rows)
            self.components.body_container.update()    
        except:
            print('exception ao atualizar tarefas 2 ')

    @update_tasks_db
    def add_tarefa(self,e):#ADDING TASK
        status='no'
        name=self.set_value(self.components.row_tasks_insert)
        
        date=str(self.components.calendario.value)[0:10]
        data_separada=date.split('-')
        data=data_separada[2]+'/'+data_separada[1]+'/'+data_separada[0]
        done="ongoing"
        
        if name:
            self.data_base.manipular_db(command='INSERT INTO tasks VALUES(?,?,?,?)', parametros=[name,data,status,done])
        self.components.description.value=''
        self.components.row_tasks_insert.update()
        
    @update_tasks_db
    def del_tarefa(self,e):#in te tasks table, the column that tells if the checkbox is selected is index number 2
        check_list=self.data_base.results
        for item in check_list:
            if item[2]=='ok':
                self.data_base.manipular_db(command='DELETE FROM tasks WHERE name = ?', parametros=[item[0]])

    @update_tasks_db
    def save_task_edit(self, e):
        new_task_name = self.components.text_field_edit_task.value

        if new_task_name != '':
            self.data_base.manipular_db(command='UPDATE tasks SET name = ? WHERE name = ?', parametros=[new_task_name, self.components.edit_data])
            if self.components.calendario.value != None:
                new_task_date=str(self.components.calendario.value)[0:10]
                data_separada=new_task_date.split('-')
                new_task_date=data_separada[2]+'/'+data_separada[1]+'/'+data_separada[0]
                self.data_base.manipular_db(command='UPDATE tasks SET date = ? WHERE name = ?', parametros=[new_task_date, new_task_name])
            self.components.text_field_edit_task.value=''
            self.components.edit_dialog_task.update()
            self.components.edit_data=new_task_name                
        else:
            if self.components.calendario.value != None:
                new_task_date=str(self.components.calendario.value)[0:10]
                data_separada=new_task_date.split('-')
                new_task_date=data_separada[2]+'/'+data_separada[1]+'/'+data_separada[0]
                self.data_base.manipular_db(command='UPDATE tasks SET date = ? WHERE name = ?', parametros=[new_task_date, self.components.edit_data]) 
                
        self.close_dialog(self.components.edit_dialog_task)
        
    def limpar_value_text_box(self,e):
        try:
            self.add_tarefa(e=e)
            self.components.description.value=''
            self.components.row_tasks_insert.update()
        except:
            print('erro ao apagar valor text box')
    
    def set_value(self,e):#SETTING VALUE 
        try:
            nome=e.controls[0].value    
        except:
            nome=e.control.value        
        return(nome)
    
    def tabs_changed(self, e):
        if e.control.selected_index == 0:
            self.view = 'all'
        elif e.control.selected_index == 1:
            self.view = 'ongoing'
        elif e.control.selected_index == 2:
            self.view = 'done'
        
        self.atualizar_tarefas()

    @update_tasks_db
    def checked(self, e):
        is_checked = e.control.value
        label = e.control.label

        if is_checked:
            self.data_base.manipular_db('UPDATE tasks SET selected = "ok" WHERE name = ?', parametros=[label])
        elif is_checked ==False :
            self.data_base.manipular_db('UPDATE tasks SET selected = "no" WHERE name = ?', parametros=[label])
            
        if self.view == 'all':
            self.data_base.results = self.data_base.manipular_db('SELECT * FROM tasks')
        else:
            self.data_base.results = self.data_base.manipular_db('SELECT * FROM tasks WHERE status = ?', parametros=[self.view])

        

    def done(self, e):
        is_checked = e.control.value
        label = e.control.label

        if is_checked ==True:
            self.data_base.manipular_db('UPDATE tasks SET status = "done" WHERE name = ?', parametros=[label])

        else:
            self.data_base.manipular_db('UPDATE tasks SET status = "ongoing" WHERE name = ?', parametros=[label])

        if self.view == 'all':
            self.results = self.data_base.manipular_db('SELECT * FROM tasks')
        else:
            self.results = self.data_base.manipular_db('SELECT * FROM tasks WHERE status = ?', parametros=[self.view])

        self.atualizar_tarefas()

    def return_checkeds_for_del(self):
        return [ft.Checkbox(
                        adaptive=True,
                        check_color=self.colors.cor_black,
                        hover_color=self.colors.cor_teal,
                        active_color=self.colors.cor_orange,
                        label=resultado[0],
                        label_style=self.colors.text_black,# type: ignore
                        label_position=ft.LabelPosition.RIGHT,
                        on_change=self.checked,
                        value=True if resultado[2]=='ok' else False
                    ) for resultado in self.data_base.results]
    
    def task_containers(self):
        containers = []
        if self.data_base.results!= []:
            for resultado in self.data_base.results:
                row= ft.Row(
                            width=5000,#TO MAKE SURE THE ROW IS AS LARGE AS THE SCREEN CAN BE, I COULDN'T FIND ANOTHER TO DO THIS, WHEN I SET EXPAND TO TRUE THE HEIGHT WAS AFFECTED AS WELL
                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            tight=True,
                            scroll=ft.ScrollMode.AUTO,
                            spacing=5,
                            controls=[
                                ft.Checkbox(
                                    check_color=self.colors.cor_black,
                                    hover_color=self.colors.cor_teal,
                                    active_color=self.colors.cor_orange,
                                    focus_color=self.colors.cor_black,
                                    label=resultado[0],
                                    label_style=self.colors.text_green if resultado[3] == "done" else self.colors.text_red,# type: ignore
                                    label_position=ft.LabelPosition.RIGHT,
                                    tooltip="Selecionar tarefa",
                                    on_change=self.checked,
                                    value=resultado[2] == 'ok'
                                ),
                                ft.Text(
                                    weight=ft.FontWeight.BOLD,
                                    color=self.colors.cor_green if resultado[3] == "done" else self.colors.cor_red,
                                    value=' até ' + resultado[1]
                                ),
                                ft.IconButton(
                                    icon=ft.icons.EDIT,
                                    icon_color=self.colors.cor_teal,
                                    on_click=self.open_dialog,
                                    data=resultado[0]
                                ),
                                ft.Checkbox(
                                    check_color=self.colors.cor_white,
                                    hover_color=self.colors.cor_teal,
                                    active_color=self.colors.cor_teal,
                                    label=resultado[0],
                                    label_position=ft.LabelPosition.RIGHT,
                                    label_style=self.colors.text_invisible_label_style,
                                    tooltip="Status da tarefa",
                                    on_change=self.done,
                                    value=resultado[3] == 'done'
                                )
                            ]
                            )
            
                containers.append(row)
            return containers
        
        else:
            return [ft.Row(
                controls=[
                    ft.Text(value='Não há tarefas nesta categoria!', color=self.colors.cor_black, style=self.colors.text_black)
                ]
            )]
