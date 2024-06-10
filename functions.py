import flet as ft

from Tracker.database import Database
from Tracker.flet_colors import Flet_colors


class Functions():

    def __init__(self,layout,components) -> None:
        #INSTANTIATING LAYOUT AND COMPONENTS CLASS USING THE SELF PARAMETER OF EXISTENT INSTANCES
        self.layout=layout
        self.components=components
        #INTANCES
        self.data_base=Database()
        self.colors=Flet_colors()
        #INITIATING VARIABLES
        self.edit_data=''
        self.task = ''

        self.layout.page.on_keyboard_event = self.handle_key_event

        self.view = 'all'
        self.atualizar_tarefas()
        
        

    def check(self,e):
        e.control.checked= not e.control.checked
        self.text_money=e.control.text
        e.control.checked= not e.control.checked
        e.control.update()
    
    #ALERT DIALOAG METHODS
    def open_dialog(self, e):
        self.edit_data=e.control.data
        self.layout.edit_dialog.open = True
        self.layout.edit_dialog.visible=True
        self.layout.page.update()

    def close_dialog(self, e):
        self.layout.edit_dialog.open= False
        self.layout.page.update()

    #EVENT HANDLER WHEN KEYBOARD IS USED
    def handle_key_event(self, event):
        # print(event.key,'tecla') Para saber como chamar a tecla pressionada
        if event.key == "Escape":
            self.close_dialog(event) 

        elif event.key =="Tab" and event.shift:
            self.layout.nav_bar.selected_index = 1 if self.layout.container_main.content == self.layout.Container_money else 0
            
            self.layout.main_tabs_change((self.layout.nav_bar))
            
        elif event.key =="Delete":
            self.del_tarefa(self.layout.row_tasks_insert.controls[3])#chamando com o icone de delete só pra padronizar

    #MAIN TABS CHANGE METHOD
    def main_tabs_change(self,e):
        try:
            if e.control.selected_index==0:
                self.layout.container_main.content=self.components.Container_money
                self.view='all_money'
                print('all')
            else:
                self.layout.container_main.content=self.components.Container_tasks
                self.view='all'
        except:
            if e.selected_index==0:
                self.layout.container_main.content=self.components.Container_money
                self.view='all_money'
            else:
                self.layout.container_main.content=self.components.Container_tasks
                self.view='all'
        self.components.nav_bar.update()
        self.components.container_main.update()
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
                print(self.components.column_tasks.controls,'controls')
                task_rows = self.task_containers()
                self.components.column_tasks.controls.extend(task_rows)
                self.components.column_tasks.update()
        except:
            print('exception ao atualizar tarefas')

    def add_tarefa(self,e):#ADDING TASK
        status='no'
        name=self.set_value(self.components.row_tasks_insert)
        
        date=str(self.components.calendario.value)[0:10]
        data_separada=date.split('-')
        data=data_separada[2]+'/'+data_separada[1]+'/'+data_separada[0]
        done="ongoing"
        
        if name:
            self.data_base.manipular_db(command='INSERT INTO tasks VALUES(?,?,?,?)', parametros=[name,data,status,done])

        self.atualizar_tarefas()

    def del_tarefa(self,e):

        check_list=self.return_checkeds_for_del()

        for item in check_list:
            if item.value==True:
                self.data_base.manipular_db(command='DELETE FROM tasks WHERE name = ?', parametros=[item.label])

        self.atualizar_tarefas()

    def save_task_edit(self, e):
        new_task_name = self.layout.text_field_edit.value

        new_task_date=str(self.layout.calendario.value)[0:10]
        data_separada=new_task_date.split('-')
        new_task_date=data_separada[2]+'/'+data_separada[1]+'/'+data_separada[0]

        self.data_base.manipular_db('UPDATE tasks SET name = ? WHERE name = ?', parametros=[new_task_name, self.edit_data])
        self.data_base.manipular_db('UPDATE tasks SET date = ? WHERE name = ?', parametros=[new_task_date, new_task_name])
        self.edit_data=new_task_name
        self.layout.text_field_edit.value=''
        self.layout.edit_dialog.update()
        self.atualizar_tarefas()
        self.close_dialog
    
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
        
        print(self.view)
        self.atualizar_tarefas()

    def checked(self, e):
        is_checked = e.control.value
        label = e.control.label

        if is_checked:
            self.data_base.manipular_db('UPDATE tasks SET selected = "ok" WHERE name = ?', parametros=[label])
        elif is_checked ==False :
            self.data_base.manipular_db('UPDATE tasks SET selected = "no" WHERE name = ?', parametros=[label])
    
        if self.view == 'all':
            self.results = self.data_base.manipular_db('SELECT * FROM tasks')
        else:
            self.results = self.data_base.manipular_db('SELECT * FROM tasks WHERE status = ?', parametros=[self.view])

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
                        tight=True,
                        scroll=ft.ScrollMode.AUTO,
                        spacing=5,
                        controls=[
                            ft.Checkbox(
                                adaptive=True,
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
                                value='até ' + resultado[1]
                            ),
                            ft.IconButton(
                                icon=ft.icons.EDIT,
                                icon_color=self.colors.cor_teal,
                                on_click=self.open_dialog,
                                data=resultado[0]
                            ),
                            ft.Checkbox(
                                adaptive=True,
                                check_color=self.colors.cor_white,
                                hover_color=self.colors.cor_teal,
                                active_color=self.colors.cor_teal,
                                label=resultado[0],
                                label_position=ft.LabelPosition.LEFT,
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