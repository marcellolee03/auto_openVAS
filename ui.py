from auto_vas_brain import AutoVASBrain
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *

class AutoVASInterface:

    def __init__(self, auto_vas_brain: AutoVASBrain):

    # ---------------------------- MONTANDO UI ------------------------------- #

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
        self.setup_autovas.grid(row=5, column=0, sticky = "ew", pady= 20)

        self.avancado = Button(text = "Opções Avançadas", command = self.opc_avancadas)
        self.avancado.grid(row=5, column=2, sticky= "ew")
        
        self.relatorios = Button(text = "Ver Relatorios", command = self.relatorio)
        self.relatorios.grid(row=5, column=1, sticky = "ew")

        self.one_click_scan_button = Button(text = "Realizar Scan", command = self.oneclick_scan)
        self.one_click_scan_button.grid(row=6, column=0, sticky = "ew", columnspan = 3)


        self.window.mainloop()

    # ---------------------------- INICIAR SETUP AUTOVAS ------------------------------- #
    
    def setup(self):
        self.senha_sudo = self.senha_sudo_entry.get()
        self.id_container = self.brain.encontrar_gmvd_id(self.senha_sudo)

        if not self.senha_sudo:
            messagebox.showinfo(title = "Erro", message = "Para realizar o setup, informe a senha do Super Usuário.")

        else:
            self.progress_window = Toplevel()
            self.progress_window.config(padx=40, pady=20)
            self.progress_window.resizable(width=False,height=False)
            self.progress_window.protocol("WM_DELETE_WINDOW", lambda: None)

            self.status_label = Label(self.progress_window, text = "Preparando o ambiente. Por favor, não feche a aplicação...", font = ("calibre", 10, "normal"))
            self.status_label.grid(row=0,column=0)

            self.f = lambda senha_sudo, id_container : (self.brain.setup_auto_openvas(senha_sudo, id_container),\
                                                        self.status_label.config(text = "Operação concluída com sucesso! A aplicação está pronta para ser utilizada"),\
                                                        self.progress_window.protocol("WM_DELETE_WINDOW", self.progress_window.destroy))

            self.window.after(100, self.f, self.senha_sudo, self.id_container)
    
    
    # ---------------------------- INICIAR ONE-CLICK SCAN ------------------------------- #

    def oneclick_scan(self):
        #Recolhendo os credenciais
        self.senha_sudo = self.senha_sudo_entry.get()
        self.senha_openvas = self.senha_openvas_entry.get()
        self.nome_task = self.nome_task_entry.get()
        self.id_container = self.brain.encontrar_gmvd_id(self.senha_sudo)


        if not self.senha_sudo or not self.senha_openvas or not self.nome_task:
            messagebox.showinfo(title = "Erro", message = "Certifique-se de não deixar nenhum campo vazio!")

        else:
            self.progress_window = Toplevel()
            self.progress_window.config(padx=20, pady=10)
            self.progress_window.resizable(width=False, height=False)

            self.bar = Progressbar(self.progress_window, orient = HORIZONTAL)
            self.bar.grid(row = 0, column = 0, pady = 15, columnspan = 2)

            self.status_label = Label(self.progress_window, text = "Encontrando o IP do gateway...", font = ("calibre", 10, "normal"))
            self.status_label.grid(row = 1, column = 0, columnspan = 2)


            #Utilizando o metodo after para dar 100ms para que a janela se forme antes do início da função
            self.progress_window.after(100, self.encontrar_gateway_ui, self.bar, self.status_label, self.senha_sudo, self.senha_openvas, self.nome_task, self.id_container)

    
        ## ---------------------------- ENCONTRAR GATEWAY ------------------------------- ##

    def encontrar_gateway_ui(self, progress_bar, status_label, senha_sudo, senha_openvas, nome_task, id_container):
        self.gateway_ip = self.brain.encontrar_gateway(senha_sudo)
        progress_bar['value'] += 20
        status_label.config(text = "Armazenando IPs de hosts conectados ao gateway...")

        #Novamente utilizando o método after para que a janela atualize antes do início da próxima função
        self.progress_window.after(100, self.armazenar_hosts_ui, progress_bar, status_label, self.gateway_ip, senha_sudo, senha_openvas, nome_task, id_container)

    
        ## ---------------------------- ARMAZENAR HOSTS ------------------------------- ##

    def armazenar_hosts_ui(self, progress_bar, status_label, gateway_ip, senha_sudo, senha_openvas, nome_task, id_container):
        self.brain.armazenar_hosts(gateway_ip)
        progress_bar['value'] += 20
        status_label.config(text = "Criando target...")

        self.progress_window.after(100, self.criar_target_ui, progress_bar, status_label, senha_sudo, senha_openvas, nome_task, id_container)


        ## ---------------------------- CRIAR TARGET ------------------------------- ##

    def criar_target_ui(self, progress_bar, status_label, senha_sudo, senha_openvas, nome_task, id_container):
        self.brain.criar_target(senha_openvas, senha_sudo, id_container)
        progress_bar['value'] += 20
        status_label.config(text = "Criando task...")

        self.progress_window.after(100, self.criar_task_ui, progress_bar,status_label, senha_sudo, senha_openvas, nome_task, id_container)
    
        ## ---------------------------- CRIAR TASK ------------------------------- ##

    def criar_task_ui(self, progress_bar, status_label, senha_sudo, senha_openvas, nome_task, id_container):
        self.brain.criar_task(senha_openvas, senha_sudo, id_container, nome_task)
        progress_bar['value'] += 20
        status_label.config(text = "Colocando scan para ser realizado...")
        
        self.progress_window.after(100, self.realizar_scan_ui, progress_bar, status_label, senha_sudo, senha_openvas, nome_task, id_container)

        ## ---------------------------- REALIZAR SCAN ------------------------------- ##

    def realizar_scan_ui(self, progress_bar, status_label, senha_sudo, senha_openvas, nome_task, id_container):
        self.brain.realizar_scan(senha_openvas, senha_sudo, id_container, nome_task)
        progress_bar['value'] += 20
        status_label.config(text = "Scan iniciado com sucesso!")
        self.progress_window.destroy()

        messagebox.showinfo(title = "Sucesso!", message = f"Operação concluída com sucesso. Task {self.nome_task} criada e iniciada!")
        

    # ---------------------------- OPÇÕES AVANÇADAS (FUNCIONALIDADE FUTURA) ------------------------------- #

    def opc_avancadas(self):
        self.window = Toplevel()
        self.window.wm_title("Opções avançadas")
        self.window.config(padx=50, pady=30)
        self.window.resizable(width=False, height=False)

        self.titulo = Label(self.window, text= "Opções Avançadas", font = ("calibre", 20, "bold"))
        self.titulo.grid(row=0,column=0, pady=30)

        self.atualizar_openvas = Button(self.window, text = "Atualizar OpenVAS")
        self.atualizar_openvas.grid(row = 1, column = 0)
   
    # ---------------------------- Ver Relatorios ------------------------------- #

    def relatorio(self):
        self.senha_sudo = self.senha_sudo_entry.get()
        self.senha_openvas = self.senha_openvas_entry.get()
        self.id_container = self.brain.encontrar_gmvd_id(self.senha_sudo)

        if not self.senha_sudo or not self.senha_openvas:
            messagebox.showinfo(title="Erro", message="Certifique-se de preencher todos os campos de senha!")
        else:
            relatorios = self.brain.gerar_relatorio(self.senha_openvas, self.senha_sudo, self.id_container)
            print("Relatórios retornados:", relatorios)

            self.window = Toplevel()
            self.window.wm_title("Ver Relatórios")
            self.window.config(padx=20, pady=20)
            self.window.resizable(width=False, height=False)

            # Cabeçalhos da tabela
            headers = ["ID", "Criação", "Modificação", "Tarefa", "Status", "Progresso", "Ação"]
            for col, texto in enumerate(headers):
                label = Label(self.window, text=texto, font=("calibre", 12, "bold"))
                label.grid(row=0, column=col, sticky="nsew", padx=5, pady=5)

            # Conteúdo dos relatórios
            for idx, relatorio in enumerate(relatorios):
                Label(self.window, text=relatorio["id"], font=("calibre", 10), wraplength=250).grid(row=idx+1, column=0, sticky="w", padx=5, pady=2)
                Label(self.window, text=relatorio["creation_time"], font=("calibre", 10)).grid(row=idx+1, column=1, padx=5, pady=2)
                Label(self.window, text=relatorio["modification_time"], font=("calibre", 10)).grid(row=idx+1, column=2, padx=5, pady=2)
                Label(self.window, text=relatorio["task_name"], font=("calibre", 10)).grid(row=idx+1, column=3, padx=5, pady=2)
                Label(self.window, text=relatorio["status"], font=("calibre", 10)).grid(row=idx+1, column=4, padx=5, pady=2)
                Label(self.window, text=relatorio["progress"], font=("calibre", 10)).grid(row=idx+1, column=5, padx=5, pady=2)

                btn_baixar = Button(self.window, text="Baixar", command=lambda rid=relatorio["id"]: self.brain.baixar_relatorio(rid, self.senha_sudo, self.id_container, self.senha_openvas))
                btn_baixar.grid(row=idx+1, column=6, padx=5, pady=2)

    

