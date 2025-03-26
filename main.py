from functions import *
from tkinter import *


# ---------------------------- FUNÇÕES ------------------------------- #

#Função para juntar todas as funções em uma
def oneclick_scan():
    senha_sudo = senha_sudo_entry.get()
    senha_openvas = senha_openvas_entry.get()
    nome_task = nome_task_entry.get()
    id_container = encontrar_gvmd_id(senha_sudo)

    criar_target(senha_openvas, senha_sudo, id_container)
    criar_task(senha_openvas, senha_sudo, id_container, nome_task)
    realizar_scan(senha_openvas, senha_sudo, id_container, nome_task)


#Função para realizar o setup do programa
def setup():
    senha_sudo = senha_sudo_entry.get()
    id_container = encontrar_gvmd_id(senha_sudo)

    setup_auto_openvas(senha_sudo, id_container)
    
# ---------------------------- UI ------------------------------- #

#window
window = Tk()
window.title("AutoVAS")
window.config(padx=50,pady=30)
window.resizable(width=False, height=False)


#logo
logo = Canvas(width=200,height=200)
logo_image = PhotoImage(file="assets/larces-01.png")
logo.create_image(100,100,image=logo_image)
logo.grid(row=0, column=0)


#labels
title_label = Label(text = "AutoVAS\nOne-click Scan", font = ("calibre", 20, "bold"))
title_label.grid(row=0, column=1, pady=20)

senha_sudo_label = Label(text = "Senha SUDO:", font = ("calibre", 10, "normal"))
senha_sudo_label.grid(row=2, column=0)

senha_openvas_label = Label(text = "Senha do OPENVAS:", font = ("calibre", 10, "normal"))
senha_openvas_label.grid(row=3, column=0)

nome_task_label = Label(text = "Nome da TASK:", font = ("calibre", 10, "normal"))
nome_task_label.grid(row=4, column=0)


#entries
senha_sudo_entry = Entry(width=36, font = ("calibre", 10, "normal"))
senha_sudo_entry.config(show='*')
senha_sudo_entry.grid(row=2, column=1, columnspan=2)

senha_openvas_entry = Entry(width=36, font = ("calibre", 10, "normal"))
senha_openvas_entry.config(show='*')
senha_openvas_entry.grid(row=3, column=1, columnspan=2)

nome_task_entry = Entry(width = 36, font = ("calibre", 10, "normal"))
nome_task_entry.grid(row=4, column=1, columnspan=2)


#button
setup_autovas = Button(text = "Setup AutoVAS", command = setup)
setup_autovas.grid(row=5, column=0, sticky = "ew")

avancado = Button(text = "Opções Avançadas")
avancado.grid(row=5, column=1, pady=20, columnspan = 2, sticky= "ew")

one_click_scan_button = Button(text = "Realizar Scan", command = oneclick_scan)
one_click_scan_button.grid(row=6, column=0, sticky = "ew", columnspan = 3)
window.mainloop()