from Tracker.database import Database

class Functions():

    def __init__(self,layout) -> None:
        self.layout=layout#INSTANTIATING LAYOUT CLASS
        self.data_base=Database()
        #INITIATING VARIABLES
        self.edit_data=''
        self.task = ''
        self.view = 'all'
        self.layout.page.on_keyboard_event = self.handle_key_event

    def check(self,e):
        e.control.checked= not e.control.checked
        self.text_money=e.control.text
        e.control.checked= not e.control.checked
        e.control.update()
    
    #EVENT HANDLER WHEN KEYBOARD IS USED
    def handle_key_event(self, event):
        # print(event.key,'tecla') Para saber como chamar a tecla pressionada
        if event.key == "Escape":
            self.close_dialog(event) 

        elif event.key =="Tab" and event.shift:
            self.nav_bar.selected_index = 1 if self.container_main.content == self.Container_money else 0
            
            self.main_tabs_change((self.nav_bar))
            
        elif event.key =="Delete":
            self.del_tarefa(self.row_tasks_insert.controls[3])#chamando com o icone de delete só pra padronizar

    #METHOD THAT AFFECTS THE TASKS
    def atualizar_tarefas(self):#METHOD TO UPDATE TASKS
        try:
            try:
                if self.column_tasks.controls[2]:
                    self.column_tasks.controls.pop()        
                    if self.view=='all':
                        self.results = self.data_base.manipular_db('SELECT * FROM tasks')

                    elif self.view=='done':
                        self.results = self.data_base.manipular_db('SELECT * FROM tasks WHERE status = "done"')
                        
                    elif self.view=='ongoing':
                        self.results = self.data_base.manipular_db('SELECT * FROM tasks WHERE status = "ongoing"')
                        
                    self.column_tasks.controls.append(self.task_containers())
                    self.column_tasks.update()    
            except:
                self.results = self.data_base.manipular_db('SELECT * FROM tasks')
                self.column_tasks.controls.append(self.task_containers())
                
                self.column_tasks.update()    
        except:
            print('exception ao atualizar tarefas')

    def add_tarefa(self,e):#ADDING TASK
        status='no'
        name=self.set_value(self.row_tasks_insert)
        
        date=str(self.calendario.value)[0:10]
        data_separada=date.split('-')
        data=data_separada[2]+'/'+data_separada[1]+'/'+data_separada[0]
        done="ongoing"
        
        if name:
            self.data_base.manipular_db(command='INSERT INTO tasks VALUES(?,?,?,?)', parametros=[name,data,status,done])

        self.atualizar_tarefas()
    
    def limpar_value_text_box(self,e):
        try:
            self.add_tarefa(e=e)
            self.description.value=''
            self.row_tasks_insert.update()
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
                        check_color=ft.colors.BLACK,
                        hover_color=ft.colors.TEAL,
                        active_color=ft.colors.ORANGE,
                        label=resultado[0],
                        label_style=black,# type: ignore
                        label_position=ft.LabelPosition.RIGHT,
                        on_change=self.checked,
                        value=True if resultado[2]=='ok' else False
                    ) for resultado in self.results]
    
    def task_containers(self):#METHOD TO CREATE A CONTAINER FOR EVERY TASK
    
        return ft.Container(
            
            expand=True,
            content=ft.Column(
                controls=
                    [
                    ft.Row(
                        tight=True,
                        scroll=ft.ScrollMode.AUTO ,
                        spacing=5,
                        controls=[
                            ft.Checkbox(
                                adaptive=True,
                                check_color=ft.colors.BLACK,
                                hover_color=ft.colors.TEAL,
                                active_color=ft.colors.ORANGE,
                                focus_color=cor_black,
                                label=resultado[0],
                                label_style=green if resultado[3]=="done" else red,# type: ignore
                                label_position=ft.LabelPosition.RIGHT,
                                tooltip="Selecionar tarefa",
                                on_change=self.checked,
                                value=True if resultado[2]=='ok' else False
                                ),
                            ft.Text(weight=ft.FontWeight.BOLD,
                                    color=cor_green if resultado[3]=="done" else cor_red,
                                    value='até '+ resultado[1]),
                            ft.IconButton(icon=ft.icons.EDIT,
                                          icon_color=ft.colors.TEAL,
                                          on_click=self.open_dialog,
                                          data=resultado[0]),
                                          
                            ft.Checkbox(
                                adaptive=True,
                                check_color=ft.colors.WHITE,
                                hover_color=ft.colors.TEAL,
                                active_color=ft.colors.TEAL,
                                label=resultado[0],
                                label_position=ft.LabelPosition.NONE,           
                                label_style=invisible_label_style, # type: ignore
                                tooltip="Status da tarefa",
                                on_change=self.done,
                                value=True if resultado[3]=='done' else False
                                )
                        ] 
                    ) for resultado in self.results
                    ],
                    scroll=ft.ScrollMode.ALWAYS 
                    )
                )

    def teste(self,e):
        print('testando chamar functions usando POO')