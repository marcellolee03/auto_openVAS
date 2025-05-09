from auto_vas_brain import AutoVASBrain
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from tkinter import simpledialog
from tkinter import filedialog


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


        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)

        #buttons
        self.setup_autovas = Button(text="Setup AutoVAS", command=self.setup)
        self.setup_autovas.grid(row=5, column=0, sticky="ew", pady=(20, 10))

        self.relatorios = Button(text="Ver Relatórios", command=self.relatorio)
        self.relatorios.grid(row=5, column=1, sticky="ew", pady=(20, 10))

        self.one_click_scan_button = Button(text="Realizar Scan", command=self.oneclick_scan)
        self.one_click_scan_button.grid(row=7, column=0, columnspan=2, sticky="ew", padx=2, pady=10)



        self.window.mainloop()

    # ---------------------------- INICIAR SETUP AUTOVAS ------------------------------- #
    
    def setup(self):
        self.senha_sudo = self.senha_sudo_entry.get()
        self.id_container = self.brain.encontrar_gmvd_id(self.senha_sudo)

        if not self.senha_sudo:
            messagebox.showinfo(title = "Erro", message = "Para realizar o setup, informe a senha do Super Usuário.")

        else:
            def setupautovas():
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

            def atualizar():
                janela.destroy()
                self.brain.atualizar_feed()

            def instalaropenvasdocker():
                janela.destroy()
                self.brain.instalar_openvas_docker()

            janela = Toplevel()
            janela.config(padx=40, pady=20)
            janela.resizable(False, False)

            label = Label(janela, text="Escolha uma opcao :", font=("calibre", 10, "normal"))
            label.pack(pady=10)

            btn_instalardocker = Button(janela, text="Instalar Docker", width=20, command=instalaropenvasdocker)
            btn_instalardocker.pack(pady=5)

            btn_setup = Button(janela, text="Preparar ambiente", width=20, command=setupautovas)
            btn_setup.pack(pady=5)

            btn_atualizar = Button(janela, text="Atualizar Feed Scan", width=20, command=atualizar)
            btn_atualizar.pack(pady=5)

    
    
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
        self.gateway_ip = self.brain.encontrar_gateway()
        print(self.gateway_ip)
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
        self.progress_window.after(100, lambda: self.analisar_progresso_scan_ui(progress_bar, status_label, nome_task))

    def analisar_progresso_scan_ui(self,progress_bar, status_label,nome_task):
        self.senha_sudo = self.senha_sudo_entry.get()
        self.senha_openvas = self.senha_openvas_entry.get()
        self.id_container = self.brain.encontrar_gmvd_id(self.senha_sudo)
        

        def checar_progresso():
            relatorios = self.brain.gerar_relatorio(self.senha_openvas, self.senha_sudo, self.id_container)
            encontrado = False

            for relatorio in relatorios:
                if relatorio["task_name"] == nome_task:
                    status = relatorio["status"]
                    progress = relatorio["progress"]

                    print(f"Status atual da task '{nome_task}': {status} - {progress}")

                    try:
                        valor_progress = int(progress.replace('%', ''))
                        progress_bar['value'] = valor_progress
                        status_label.config(text=f"Status: {status} - Progresso: {progress}")
                    except ValueError:
                        print("Erro ao converter progresso para inteiro.")

                    if progress == "100%" and status == "Done":
                        print("Scan completo! Gerando Relatório Agora...")
                        self.salvar_relatorio(relatorio["id"], self.senha_sudo, self.id_container, self.senha_openvas, usar_csv=True, task_name=nome_task)
                        messagebox.showinfo(title = "Sucesso!", message = f"Operação concluída com sucesso. Task {self.nome_task} foi salva em relatorios/csv_bruto!")
                        return 
                    encontrado = True
                    break

            if not encontrado:
                print(f"Task '{nome_task}' não encontrada ainda...")

            # Marca para checar de novo em 60 segundos
            self.progress_window.after(60000, checar_progresso)

        status_label.config(text="Scan Em Progresso...")
        progress_bar['value'] = 0
        checar_progresso()
            
   
    # ---------------------------- Ver Relatorios ------------------------------- #
    def salvar_relatorio(self, relatorio_id, senha_sudo: str, id_container: str, senha_openvas: str, usar_csv: bool, task_name: str):
        nome_do_arquivo = task_name
        self.brain.baixar_relatorio(relatorio_id, senha_sudo, id_container, senha_openvas, nome_do_arquivo, usar_csv)

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
            headers = [ "Tarefa","Criação", "Status", "Progresso", "Baixar"]
            for col, texto in enumerate(headers):
                label = Label(self.window, text=texto, font=("calibre", 12, "bold"))
                label.grid(row=0, column=col, sticky="nsew", padx=5, pady=5)
                self.filtrar_arquivo = Button(self.window, text = "Selecionar Arquivo Externo e Filtrar",command=lambda :self.filtrar_csv_funcao(task_name="unknow", externo=True))
                self.filtrar_arquivo.grid(row = 0, column = 5, pady = 2,padx=5, columnspan = 3)

            # Conteúdo dos relatórios
            for idx, relatorio in enumerate(relatorios):
                Label(self.window, text=relatorio["task_name"], font=("calibre", 10)).grid(row=idx+1, column=0, padx=5, pady=2)
                Label(self.window, text=relatorio["creation_time"], font=("calibre", 10)).grid(row=idx+1, column=1, padx=5, pady=2)
                Label(self.window, text=relatorio["status"], font=("calibre", 10)).grid(row=idx+1, column=2, padx=5, pady=2)
                Label(self.window, text=relatorio["progress"], font=("calibre", 10)).grid(row=idx+1, column=3, padx=5, pady=2)


                btn_filtrar_csv = Button(
                    self.window,text="CSV Filtrado",command=lambda task_name=relatorio["task_name"]: (self.salvar_relatorio(relatorio["id"], self.senha_sudo, self.id_container, self.senha_openvas, usar_csv=True, task_name=task_name),
                            self.filtrar_csv_funcao(task_name=task_name))
                    )
                btn_filtrar_csv.grid(row=idx+1, column=4, padx=5, pady=2)

                btn_baixar_csv = Button(
                    self.window,
                    text="CSV Bruto",
                    command=lambda rid=relatorio["id"], task_name=relatorio["task_name"]: (self.salvar_relatorio(
                        rid,
                        self.senha_sudo, 
                        self.id_container, 
                        self.senha_openvas, 
                        usar_csv=True, 
                        task_name=task_name),
                        messagebox.showinfo(
                            title="Sucesso!", 
                            message=f"Operação concluída com sucesso. Task {task_name} foi salva em relatorios/csv_bruto!"
                        )
                    )
                ) 
                btn_baixar_csv.grid(row=idx+1, column=5, padx=5, pady=2)

                btn_baixar_excel = Button(
                    self.window,
                    text="Excel",
                    command=lambda rid=relatorio["id"], task_name=relatorio["task_name"]: [
                        self.salvar_relatorio(rid, self.senha_sudo, self.id_container, self.senha_openvas, usar_csv=False, task_name=task_name),
                        messagebox.showinfo(
                            title="Sucesso!", 
                            message=f"Operação concluída com sucesso. Task {task_name} foi salva em relatorios/xlsx!"
                        )
                    ]
                )
                btn_baixar_excel.grid(row=idx+1, column=6, padx=5, pady=2)


    # ---------------------------- Filtrar csv ------------------------------- #

    def filtrar_csv_funcao(self, task_name, externo=False):
        self.window = Toplevel()
        self.window.config(padx=50, pady=30)
        self.window.resizable(width=False, height=False)

        colunas = ['IP', 'Hostname', 'Port', 'Port Protocol', 'CVSS', 'Severity', 'QoD', 'Solution Type', 'NVT Name', 'Summary', 'Specific Result', 'NVT QID',\
                   'CVEs', 'Task ID', 'Task Name', 'Timestamp', 'Result ID', 'Impact', 'Solution', 'Affected Software/OS', 'Vulnerability Insight',\
                    'Vulnerability Detection Method', 'Product Detection Result', 'BIDs', 'CERTs']
        
        filtros = []
        vars = []

        for _ in range(0, len(colunas)):
            vars.append(IntVar())


        filtros_label = Label(self.window, text = "Selecione Filtros", font = ("calibre", 18, "bold"))
        filtros_label.grid(row = 0, column = 0, pady= (0, 20))

        self.todos_selecionados = False

        def toggle_selecionar_todos():
            self.todos_selecionados = not self.todos_selecionados
            for i, var in enumerate(vars):
                var.set(1 if self.todos_selecionados else 0)
            self.add_item(vars, filtros, colunas)

        botao_toggle = Button(self.window, text="Selecionar/Desmarcar Todos", command=toggle_selecionar_todos)
        botao_toggle.grid(row=1, column=0, columnspan=2, pady=(0, 20)) 


        i = 0
        j = 0
        k = 2
        for name in colunas:
            button = Checkbutton(self.window, text = name, variable = vars[i], onvalue = 1, offvalue = 0, command = lambda: self.add_item(vars, filtros, colunas))

            if i == 8:
                j = 0
                k += 1
            
            if i == 16:
                j = 0
                k += 1
        
            button.grid(row = k, column = j, pady = 5, padx = 3)

            j += 1
            i += 1

        self.filtrar_arquivo = Button(self.window, text = "Filtrar", command=lambda: self.filtrar_relatorio(filtros, task_name) if not externo else self.filtrar_relatorio_externo(filtros))
        self.filtrar_arquivo.grid(row = 5, column = 7, pady = (20, 0), columnspan = 2)


    

    def filtrar_relatorio(self, filtros: list, task_name: str):

        nome_do_arquivo = f"{task_name}_filtrado" 
        caminho= f"relatorios/csv_bruto/{task_name}.csv"

        self.brain.filtrar_csv(filtros, nome_do_arquivo, caminho)

        messagebox.showinfo(title = "Sucesso!", message = f"Arquivo {nome_do_arquivo} criado com sucesso! Salvo em relatorios/filtrado.")
        self.window.destroy()

    def filtrar_relatorio_externo(self, filtros: list):
        self.window.withdraw()

        tipos_arquivo = [("CSV files", "*.csv")]

        caminho = filedialog.askopenfilename(
            title="Selecione um arquivo CSV",
            filetypes=tipos_arquivo
        )

        nome_do_arquivo = simpledialog.askstring(title = "Nomeie o arquivo", prompt = "Digite o nome do arquivo:")

        self.brain.filtrar_csv(filtros, nome_do_arquivo, caminho)

        messagebox.showinfo(title = "Sucesso!", message = f"Arquivo {nome_do_arquivo} criado com sucesso! Salvo em relatorios/filtrado.")

    
    def add_item(self, vars:list, filtros: list, colunas: list):

        selecionados = {colunas[i] for i, var in enumerate(vars) if var.get() == 1}

        filtros.clear()
        filtros.extend(selecionados)
    
        print(filtros)


