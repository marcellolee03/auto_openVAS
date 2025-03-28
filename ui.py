from auto_vas_brain import AutoVASBrain
from tkinter import *

class AutoVASInterface:

    def __init__(self, auto_vas_brain: AutoVASBrain):

        #Funções
        self.brain = auto_vas_brain

        #Janela
        self.window = Tk()
        self.window.title("AutoVAS")
        self.window.config(padx=50,pady=30)
        self.window.resizable(width=False, height=False)

        #Logo
        self.logo = Canvas(width=200, height=200)
        self.logo_image = PhotoImage(file = "assets/larces-01.png")
        self.logo.create_image(100,100,image=self.logo_image)
        self.logo.grid(row=0, column=0)

        #Labels
        self.title_label = Label(text = "AutoVAS\nOne-click Scan", font = ("calibre", 20, "bold"))
        self.title_label.grid(row=0, column=1, pady=20)

        self.senha_sudo_label = Label(text = "Senha do SuperUser:", font = ("calibre", 10, "normal"))
        self.senha_sudo_label.grid(row=2, column=0)

        self.senha_openvas_label = Label(text = "Senha do OpenVAS:", font = ("calibre", 10, "normal"))
        self.senha_openvas_label.grid(row=3, column=0)

        self.nome_task_label = Label(text = "Nome da Task:", font = ("calibre", 10, "normal"))
        self.nome_task_label.grid(row=4, column=0)

        #Entradas
        self.senha_sudo_entry = Entry(width=36, font = ("calibre", 10, "normal"))
        self.senha_sudo_entry.config(show='*')
        self.senha_sudo_entry.grid(row=2, column=1, columnspan=2)

        self.senha_openvas_entry = Entry(width=36, font = ("calibre", 10, "normal"))
        self.senha_openvas_entry.config(show='*')
        self.senha_openvas_entry.grid(row=3, column=1, columnspan=2)

        self.nome_task_entry = Entry(width = 36, font = ("calibre", 10, "normal"))
        self.nome_task_entry.grid(row=4, column=1, columnspan=2)

        #button
        self.setup_autovas = Button(text = "Setup AutoVAS", command = self.setup)
        self.setup_autovas.grid(row=5, column=0, sticky = "ew")

        self.avancado = Button(text = "Opções Avançadas", command = self.opc_avancadas)
        self.avancado.grid(row=5, column=1, pady=20, columnspan = 2, sticky= "ew")

        self.one_click_scan_button = Button(text = "Realizar Scan", command = self.oneclick_scan)
        self.one_click_scan_button.grid(row=6, column=0, sticky = "ew", columnspan = 3)


        self.window.mainloop()

    
    def setup(self):
        self.senha_sudo = self.senha_sudo_entry.get()
        self.id_container = self.brain.encontrar_gmvd_id(self.senha_sudo)

        self.setup_auto_openvas(self.senha_sudo, self.id_container)
    

    def oneclick_scan(self):
        self.senha_sudo = self.senha_sudo_entry.get()
        self.senha_openvas = self.senha_openvas_entry.get()
        self.nome_task = self.nome_task_entry.get()
        self.id_container = self.brain.encontrar_gmvd_id(self.senha_sudo)
        
        self.brain.criar_target(self.senha_openvas, self.senha_sudo, self.id_container)
        self.brain.criar_task(self.senha_openvas, self.senha_sudo, self.id_container, self.nome_task)
        self.brain.realizar_scan(self.senha_openvas, self.senha_sudo, self.id_container, self.nome_task)
    

    def opc_avancadas(self):
        self.window = Toplevel()
        self.window.wm_title("Opções avançadas")
        self.window.config(padx=50, pady=30)
        self.window.resizable(width=False, height=False)

        self.titulo = Label(self.window, text= "Opções Avançadas", font = ("calibre", 20, "bold"))
        self.titulo.grid(row=0,column=0, pady=30)

        self.atualizar_openvas = Button(self.window, text = "Atualizar OpenVAS")
        self.atualizar_openvas.grid(row = 1, column = 0)