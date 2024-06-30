import flet as ft

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
        self.atualizar_tarefas()
        self.atualizar_money()
        
    @staticmethod
    def update_tasks_db(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return  self.atualizar_tarefas(),func(self, *args, **kwargs), self.atualizar_tarefas()
        return wrapper
    
    @staticmethod
    def update_money_db(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return self.atualizar_money(),func(self, *args, **kwargs), self.atualizar_money()
            
        return wrapper
    
    def check(self,e):#check the category of money transaction to add a new transaction
        e.control.checked= not e.control.checked
        self.text_money=e.control.text
        e.control.checked= not e.control.checked
        e.control.update()
    
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
        print(self.components.edit_data_money,'valor da transaction')

    def close_dialog_money(self, e):
        self.components.edit_dialog_money.open= False
        self.layout.page.update()

    #EVENT HANDLER WHEN KEYBOARD IS USED
    def handle_key_event(self, event):
        # print(event.key,'tecla') #Para saber como chamar a tecla pressionada
        if event.key == "Escape":
            self.close_dialog(event) 

        elif event.key =="Tab" and event.shift:
            self.components.nav_bar.selected_index = 1 if self.components.container_main.content == self.components.Container_money else 0
            self.main_tabs_change((self.components.nav_bar))
            
        elif event.key =="Delete":
            if self.components.nav_bar.selected_index==0:
                self.del_transaction(self.components.row_money_insert.controls[5])
            else:
                self.del_tarefa(self.components.row_tasks_insert.controls[3])#chamando com o icone de delete só pra padronizar

    #MAIN TABS CHANGE METHOD
    def main_tabs_change(self,e):
        try:
            if self.components.nav_bar.selected_index==0:
                self.components.container_main.content=self.components.Container_money
                self.view='all_money'
    
            else:
                self.components.container_main.content=self.components.column_tasks
                self.view='all'
            
        except:
            if self.components.nav_bar.selected_index==0:
                self.components.container_main.content=self.components.Container_money
                self.view='all_money'
            else:
                self.components.container_main.content=self.components.column_tasks
                self.view='all'

        self.components.nav_bar.update()
        self.components.container_main.update()

    #METHOD THAT AFFECTS THE MONEY
    def money_containers(self):
        money_rows_containers=[]
        for transaction in self.data_base.transactions:
            print(transaction)
            row_money= ft.Row(
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
            print(money_rows_containers) 
        return money_rows_containers

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
            print('aqui0')
            try:
                if self.components.column_money.controls[2]:
                    print('aqqui')
                    self.components.column_money.controls = self.components.column_money.controls[:2]       
                    print('aqqui2')
                    if self.view=='all_money' or self.view=="all":
                        self.data_base.transactions = self.data_base.manipular_db('SELECT * FROM money')
                        print('aqqui3')
                    elif self.view=='positive':
                        self.data_base.transactions = self.data_base.manipular_db('SELECT * FROM money WHERE value > 0;')
                        print('aqqui4')
                    elif self.view=='negative':
                        self.data_base.transactions = self.data_base.manipular_db('SELECT * FROM money WHERE value < 0;')
                        print('aqqui5')
                    money_rows=self.money_containers()
                    print('aqqui6')
                    self.components.column_money.controls.extend(money_rows)
                    print('aqqui7')
                    self.components.column_money.update()   
                    print('aqqui8')
                    self.components.Container_money.update() 
                    print('aqqui9')
            except:
                print('aqui00')
                money_rows=self.money_containers()
                print('aqqui10')
                self.components.column_money.controls.extend(money_rows)
                print('aqqui11')
                self.components.column_money.update()   
                print('aqqui12')
                self.components.Container_money.update() 
                print('aqqui13')
        except:
            print('exception ao atualizar money')

    @update_money_db
    def add_transaction(self,e):
        value_money=(self.components.value_money.data)
        value_money=int(value_money)

        selected='no'
        description=self.set_value_money(self.components.row_money_insert)
        category=self.text_money
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
    def save_task_edit_money(self, e):
        new_transaction_name = self.components.text_field_edit.value
        print(new_transaction_name,'name money')
        new_transaction_value= int(self.components.value_edit_money.value)
        print(new_transaction_value,'value money')
        new_money_date=str(self.components.calendario.value)[0:10]
        print(new_money_date,'date money')
        data_separada=new_money_date.split('-')
        new_money_date=data_separada[2]+'/'+data_separada[1]+'/'+data_separada[0]
        print(new_money_date,'data separada')
        print(self.components.edit_data_money,'variavél que guarda o nome da transaction a ser editada')
        self.data_base.manipular_db('UPDATE money SET description = ? WHERE description = ?', parametros=[new_transaction_name, self.components.edit_data_money])
        self.data_base.manipular_db('UPDATE money SET value = ? WHERE description = ?', parametros=[new_transaction_value, new_transaction_name])
        self.data_base.manipular_db('UPDATE money SET date = ? WHERE description = ?', parametros=[new_money_date, new_transaction_name])
        self.components.edit_data_money=new_transaction_name
        print(self.components.edit_data_money, 'novo nome da transaction')
        self.components.text_field_edit.value=''
        print(self.components.text_field_edit.value,'limpando valor do input do nome')
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
                if self.components.column_tasks.controls[2]:
                    self.components.column_tasks.controls = self.components.column_tasks.controls[:2]     

                    if self.view=='all':
                        self.data_base.results = self.data_base.manipular_db('SELECT * FROM tasks')
                    elif self.view=='done':
                        self.data_base.results = self.data_base.manipular_db('SELECT * FROM tasks WHERE status = "done"')
                    elif self.view=='ongoing':
                        self.data_base.results = self.data_base.manipular_db('SELECT * FROM tasks WHERE status = "ongoing"')

                    task_rows = self.task_containers()
                    self.components.column_tasks.controls.extend(task_rows)
                    self.components.column_tasks.update()
            except:
                task_rows = self.task_containers()
                self.components.column_tasks.controls.extend(task_rows)
                self.components.column_tasks.update()
        except:
            print('exception ao atualizar tarefas')

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
        new_task_name = self.components.text_field_edit.value
        print(new_task_name,'nome novo retirado do alertdialog')
        print('nome antigo da task',self.components.edit_data, 'nome antigo da task')

        new_task_date=str(self.components.calendario.value)[0:10]
        data_separada=new_task_date.split('-')
        new_task_date=data_separada[2]+'/'+data_separada[1]+'/'+data_separada[0]
        print(new_task_date,'data nova retirada do alertdialog')
        self.data_base.manipular_db(command='UPDATE tasks SET name = ? WHERE name = ?', parametros=[new_task_name, self.components.edit_data])
        print('atualizou o nome')
        self.data_base.manipular_db(command='UPDATE tasks SET date = ? WHERE name = ?', parametros=[new_task_date, new_task_name])
        print('atualizou a data')
        self.components.edit_data=new_task_name
        print(self.components.edit_data, 'novo nome da task')
        self.components.text_field_edit.value=''
        print(self.components.text_field_edit.value,'limpando valor do input do nome')
        print('atualizando componente do alert')
        self.close_dialog(self.components.edit_dialog_task)
        print('fechando alert')#copiar esse tipo de edição no caso do money, adicionando a edição de categoria
        

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
        for resultado in self.data_base.results:
            row= ft.Row(
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

                

    def teste(self,e):
        print('testando chamar functions usando POO')