import subprocess
import tempfile
import os
from re import search, MULTILINE
import re
from tkinter import filedialog


class AutoVASBrain:

    def __init__(self):
        pass
    
    # ---------------------------- FUNÇÃO AUXILIAR ------------------------------- #

    def exec_script_temp(self, script, senha_sudo):

        with tempfile.NamedTemporaryFile(mode="w", delete = False, suffix=".sh") as temp_script:
            temp_script.write(script)
            temp_script_path = temp_script.name

        try:
            comando = f'echo {senha_sudo} | sudo -S bash {temp_script_path}'
            subprocess.run(comando, shell=True, text=True)
        
        finally:
            if os.path.exists(temp_script_path):
                os.remove(temp_script_path)
    
    # ---------------------------- SETUP INICIAL ------------------------------- #

    # Move os scripts para um diretorio dentro do container do gvmd, depois cria um ambiente próprio para que estes possam ser executados
    # (cria ambiente virtual, instala pip, instala dependencias e cria um usuário não root para executar o comando 'gvm-script')

    def setup_auto_openvas(self, senha_sudo:str, id_container:str):
        script = f'''
        #!/bin/bash

        apt install traceroute
        apt install nmap

        docker exec -i greenbone-community-edition-gvmd-1 bash -c "mkdir auto_vas"

        docker cp scripts/CreateTarget/create-targets-from-host-list.gmp.py {id_container}:/auto_vas/create-targets-from-host-list.gmp.py
        docker cp scripts/CreateTask/create-tasks-from-csv.gmp.py {id_container}:/auto_vas/create-tasks-from-csv.gmp.py
        docker cp scripts/RunScan/start-scans-from-csv.py {id_container}:/auto_vas/start-scans-from-csv.py
        docker cp scripts/ListReports/list-reports.gmp.py {id_container}:/auto_vas/list-reports.gmp.py
        docker cp scripts/ListReports/export-pdf-report.gmp.py {id_container}:/auto_vas/export-pdf-report.gmp.py
        docker cp scripts/ListReports/export-xml-report.gmp.py {id_container}:/auto_vas/export-xml-report.gmp.py
        docker cp scripts/ListReports/list-reports.gmp.py {id_container}:/auto_vas/list-reports.gmp.py


        docker exec -i greenbone-community-edition-gvmd-1 bash -c "apt-get update && apt-get install -y python3-venv python3-pip"
        docker exec -i greenbone-community-edition-gvmd-1 bash -c "python3 -m venv path/to/venv && \
            source /path/to/venv/bin/activate && \
            pip install --upgrade pip && \
            pip install python-gvm gvm-tools && \
            pip install OpenVAS-Reporting && \
            pip install pyyaml && \
            pip install defusedxml"
        docker exec -i greenbone-community-edition-gvmd-1 bash -c "useradd auto_vas -s /bin/bash"
        '''

        with tempfile.NamedTemporaryFile(mode="w",delete = False, suffix=".sh") as temp_script:
            temp_script.write(script)
            temp_script_path = temp_script.name
    
        comando = f'echo {senha_sudo} | sudo -S bash {temp_script_path}'

        subprocess.run(comando, shell=True, text=True)


    # ---------------------------- ENCONTRAR ID DO CONTAINER ------------------------------- #


    def encontrar_gmvd_id(self, senha_sudo:str):
        
        comando = f'echo {senha_sudo} | sudo -S docker ps -q -f name=greenbone-community-edition-gvmd-1'
        id = subprocess.run(comando, capture_output=True, text=True, shell=True).stdout.strip()

        return id
    

    # ---------------------------- ARMAZENAR IPS ATIVOS ------------------------------- #


    # Cria um .txt contendo o IP do gateway e todos os hosts conectados a ele neste exato momento
    # Utiliza traceroute e nmap


        ## ---------------------------- ENCONTRAR GATEWAY ------------------------------- ##


    def encontrar_gateway(self, senha_sudo:str):

        # Executando o traceroute e capturando a saída

        comando = f'echo {senha_sudo} | sudo -S traceroute -I google.com'

        saida_traceroute = subprocess.run(comando, shell=True, capture_output=True, text=True)
        saida_traceroute = saida_traceroute.stdout


        # Pegando o primeiro IP da lista (Gateway)
        match = search(r'\n\s*1\s+_gateway\s+\((\d+\.\d+\.\d+\.\d+)\)', saida_traceroute)

        if match:
            gateway_ip = match.group(1)
            print(f"Gateway encontrado: {gateway_ip}")
            return gateway_ip
        
        else:
            print("Erro. Gateway não encontrado.")


        ## ---------------------------- ARMAZENAR IPs ------------------------------- ##


    def armazenar_hosts(self, gateway_ip: str):
        # Comando Nmap para escanear a rede do Gateway
            comando_nmap = f"nmap -sn -n {gateway_ip}/24 | grep 'Nmap scan report'" + "| awk '{print $5}' | paste -sd ','"

            # Executando o Nmap e armazenando os IPs
            resultado = subprocess.run(comando_nmap, shell=True, capture_output=True, text=True)
            ips_ativos = resultado.stdout.strip()

            # Salvando os IPs no arquivo lista_IPs.txt
            with open("IPs/lista_IPs.txt", "w") as file:
                file.write(ips_ativos)
                print("Hosts armazenados com sucesso!")
            

    # ---------------------------- CRIAR TARGET ------------------------------- #


    # Determina o IP do gateway e o de todos os hosts conectados a ele no momento e cria um TARGET com estes IPs

    def criar_target(self, senha_openvas: str, senha_sudo: str, id_container: str):

        script = f'''
        #!/bin/bash

        docker cp IPs/lista_IPs.txt {id_container}:/auto_vas/lista_IPs.txt

        docker exec -i --user auto_vas greenbone-community-edition-gvmd-1 bash -c "
            source /path/to/venv/bin/activate &&
            cd auto_vas &&
            gvm-script --gmp-username admin --gmp-password {senha_openvas} socket create-targets-from-host-list.gmp.py teste lista_IPs.txt"

        '''

        self.exec_script_temp(script, senha_sudo)


    # ---------------------------- CRIAR TASK ------------------------------- #



    # Cria task com o último target criado.

    def criar_task(self, senha_openvas: str, senha_sudo: str, id_container: str, nome_task: str):

        # Recebendo os últimos IPs criados
        with open("IPs/lista_IPs.txt", "r") as file:
            target_hosts = file.read()

        # Criando um .csv no padrão do script
        csv_content = f'"{nome_task}","Target for {target_hosts}","OpenVAS Default","Full and fast",,,,,,,'

        # Atualizando o .csv para criar uma task com o último TARGET criado
        with open("scripts/CreateTask/task.csv", "w") as file:
            file.write(csv_content)
    
        script = f'''#!/bin/bash

        docker cp scripts/CreateTask/task.csv {id_container}:/auto_vas/task.csv

        docker exec -i --user auto_vas greenbone-community-edition-gvmd-1 bash -c "
            source /path/to/venv/bin/activate &&
            cd auto_vas &&
            gvm-script --gmp-username admin --gmp-password {senha_openvas} socket create-tasks-from-csv.gmp.py task.csv"
        '''

        self.exec_script_temp(script, senha_sudo)
    

    # ---------------------------- REALIZAR SCAN ------------------------------- #



    def realizar_scan(self, senha_openvas: str, senha_sudo: str,  id_container:str , nome_task: str):

        with open("scripts/RunScan/startscan.csv", "w") as file:
            content = f'"{nome_task}"'
            file.write(content)

        script = f'''
        #!/bin/bash

        docker cp scripts/RunScan/startscan.csv {id_container}:/auto_vas/startscan.csv

        docker exec -i --user auto_vas greenbone-community-edition-gvmd-1 bash -c "
            source /path/to/venv/bin/activate &&
            cd auto_vas &&
            gvm-script --gmp-username admin --gmp-password {senha_openvas} socket start-scans-from-csv.py startscan.csv"

        '''

        self.exec_script_temp(script, senha_sudo)
        

    
        # ---------------------------- Fazer Relatorio ------------------------------- #


    def escolher_local_arquivo(self):

        caminho = filedialog.asksaveasfilename(
            title="Salvar relatório como",
            defaultextension=".xlsx",
            filetypes=[("XLSX files", "*.xlsx"), ("Todos os arquivos", "*.*")]
        )

        return caminho




    def gerar_relatorio(self, senha_openvas: str, senha_sudo: str, id_container: str):
        script = f'''
        docker exec -i --user auto_vas {id_container} bash -c "source /path/to/venv/bin/activate && cd auto_vas && gvm-script --gmp-username admin --gmp-password {senha_openvas} socket list-reports.gmp.py"
        '''

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".sh") as temp_script:
            temp_script.write(script)
            temp_script_path = temp_script.name

        try:
            comando = f'echo {senha_sudo} | sudo -S bash {temp_script_path}'
            resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
            saida = resultado.stdout
            print("Saída bruta do comando:\n", saida)  # Debug

        finally:
            if os.path.exists(temp_script_path):
                os.remove(temp_script_path)

        # Parse da saída
        linhas = saida.strip().splitlines()

        relatorios = []
        for linha in linhas:
            # Ignora cabeçalhos e linhas separadoras
            if linha.strip().startswith("#") or linha.strip().startswith("-") or linha.strip() == "":
                continue

            partes = [parte.strip() for parte in linha.split("|")]
            if len(partes) < 7:
                continue  # Linha incompleta, pula

            relatorio = {
                "id": partes[1],
                "creation_time": partes[2],
                "modification_time": partes[3],
                "task_name": partes[4],
                "status": partes[5],
                "progress": partes[6]
            }
            relatorios.append(relatorio)

        print("Relatórios capturados:", relatorios)  # Debug

        return relatorios


    def baixar_relatorio(self, relatorio_id, senha_sudo: str, id_container: str, senha_openvas):
        caminho_arquivo = self.escolher_local_arquivo()

        if not caminho_arquivo:
            print("Operação cancelada pelo usuário.")
            return

        # Pega apenas o nome do arquivo com extensão para passar no comando
        nome_arquivo = caminho_arquivo.split("/")[-1]

        script = f'''
        #!/bin/bash
        docker exec {id_container} bash -c "chmod 777 /auto_vas"
        
        docker exec --user auto_vas {id_container} bash -c "source /path/to/venv/bin/activate && cd auto_vas && gvm-script --gmp-username admin --gmp-password {senha_openvas} socket export-xml-report.gmp.py {relatorio_id} pretty_relatorio\
            && openvasreporting -i pretty_relatorio.xml"
        docker cp {id_container}:/auto_vas/openvas_report.xlsx  "{caminho_arquivo}"
        '''

        self.exec_script_temp(script, senha_sudo)

        print(f"Relatório sendo salvo em: {caminho_arquivo}") 
    
   
   
