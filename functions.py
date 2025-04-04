import subprocess
from re import search, MULTILINE
import tempfile

# ---------------------------- ENCONTRAR ID DO CONTAINER ------------------------------- #

def encontrar_gvmd_id(senha_sudo: str):

    id = subprocess.run(["sudo", "-S", "docker", "ps", "-q", "-f", "name=greenbone-community-edition-gvmd-1"], capture_output=True, text=True, input=senha_sudo +"\n").stdout.strip()
    return id


# ---------------------------- SETUP INICIAL ------------------------------- #

# Move os scripts para um diretorio dentro do container do gvmd, depois cria um ambiente próprio para que estes possam ser executados
# (cria ambiente virtual, instala pip, instala dependencias e cria um usuário não root para executar o comando 'gvm-script')
def setup_auto_openvas(senha_sudo: str, id_container: str):

    script_mover_arquivos = f'''
#!/bin/bash


sudo -S docker exec -it greenbone-community-edition-gvmd-1 mkdir -p autovas
sudo -S docker cp scripts/CreateTarget/create-targets-from-host-list.gmp.py {id_container}:/auto_vas/create-targets-from-host-list.gmp.py
sudo -S docker cp scripts/CreateTask/create-tasks-from-csv.gmp.py {id_container}:/auto_vas/create-tasks-from-csv.gmp.py
sudo -S docker cp scripts/RunScan/start-scans-from-csv.py {id_container}:/auto_vas/start-scans-from-csv.py
'''

    with open("scripts/setup/mover-arquivos.sh", "w") as file:
        file.write(script_mover_arquivos)

    env = {"SUDO_ASKPASS": "/bin/echo"} 
    subprocess.run(["sudo", "-S", "./scripts/setup/mover-arquivos.sh"], input=senha_sudo + "\n", text=True, env=env)
    subprocess.run(["sudo", "-S", "./scripts/setup/criar-ambiente.sh"], input=senha_sudo + "\n", text=True, env=env)

# ---------------------------- CRIAR TARGET ------------------------------- #

# Determina o IP do gateway e o de todos os hosts conectados a ele no momento e cria um TARGET com estes IPs
def criar_target(senha_openvas: str, senha_sudo: str, id_container: str):
    gerar_txt_ip()

    script = f'''
#!/bin/bash

sudo docker cp IPs/lista_IPs.txt {id_container}:/auto_vas/lista_IPs.txt

sudo docker exec -i --user auto_vas greenbone-community-edition-gvmd-1 bash -c "
    source /path/to/venv/bin/activate &&
    cd auto_vas &&
    gvm-script --gmp-username admin --gmp-password {senha_openvas} socket create-targets-from-host-list.gmp.py teste lista_IPs.txt"

'''

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".sh") as temp_script:
        temp_script.write(script)
        temp_script_path = temp_script.name
    
    comando = f'echo {senha_sudo} | sudo -S bash {temp_script_path}'

    subprocess.run(comando, shell=True, text=True)

# ---------------------------- CRIAR TASK ------------------------------- #


# Cria task com o último target criado.
def criar_task(senha_openvas: str, senha_sudo: str, id_container: str, nome_task: str):

    # Recebendo os últimos IPs criados
    with open("IPs/lista_IPs.txt", "r") as file:
        target_hosts = file.read()

    # Criando um .csv no padrão do script
    csv_content = f'"{nome_task}","Target for {target_hosts}","OpenVAS Default","Full and fast",,,,,,,'

    # Atualizando o .csv para criar uma task com o último TARGET criado
    with open("scripts/CreateTask/task.csv", "w") as file:
        file.write(csv_content)
    
    script = f'''#!/bin/bash

sudo docker cp scripts/CreateTask/task.csv {id_container}:/auto_vas/task.csv

sudo docker exec -i --user auto_vas greenbone-community-edition-gvmd-1 bash -c "
    source /path/to/venv/bin/activate &&
    cd auto_vas &&
    gvm-script --gmp-username admin --gmp-password {senha_openvas} socket create-tasks-from-csv.gmp.py task.csv"
'''

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".sh") as temp_script:
        temp_script.write(script)
        temp_script_path = temp_script.name
    
    comando = f'echo {senha_sudo} | sudo -S bash {temp_script_path}'

    subprocess.run(comando, shell=True, text=True)
    

# ---------------------------- REALIZAR SCAN ------------------------------- #

def realizar_scan(senha_openvas: str, senha_sudo: str,  id_container:str , nome_task: str):

    with open("scripts/RunScan/startscan.csv", "w") as file:
        content = f'"{nome_task}"'
        file.write(content)

    script = f'''
#!/bin/bash

sudo docker cp scripts/RunScan/startscan.csv {id_container}:/auto_vas/startscan.csv

sudo docker exec -i --user auto_vas greenbone-community-edition-gvmd-1 bash -c "
    source /path/to/venv/bin/activate &&
    cd auto_vas &&
    gvm-script --gmp-username admin --gmp-password {senha_openvas} socket start-scans-from-csv.py startscan.csv"

'''
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".sh") as temp_script:
        temp_script.write(script)
        temp_script_path = temp_script.name
    
    comando = f'echo {senha_sudo} | sudo -S bash {temp_script_path}'

    subprocess.run(comando, shell=True, text=True)

# ---------------------------- ARMAZENAR IPS ATIVOS ------------------------------- #

# Cria um .txt contendo o IP do gateway e todos os hosts conectados a ele neste exato momento
# Utiliza traceroute e nmap
def gerar_txt_ip():
    # Executando o traceroute e capturando a saída
    saida_traceroute = subprocess.run("traceroute -n google.com", shell=True, capture_output=True, text=True)
    saida_traceroute = saida_traceroute.stdout

    # Pegando o primeiro IP da lista (Gateway)
    match = search(r"^\s*1\s+([\d.]+)", saida_traceroute, MULTILINE)

    if match:
        gateway_ip = match.group(1)
        print(f"Gateway encontrado: {gateway_ip}")

        # Comando Nmap para escanear a rede do Gateway
        comando_nmap = f"nmap -sn -n {gateway_ip}/24 | grep 'Nmap scan report'" + "| awk '{print $5}' | paste -sd ','"

        # Executando o Nmap e armazenando os IPs
        resultado = subprocess.run(comando_nmap, shell=True, capture_output=True, text=True)
        ips_ativos = resultado.stdout.strip()

        # Salvando os IPs no arquivo lista_IPs.txt
        with open("IPs/lista_IPs.txt", "w") as file:
            file.write(ips_ativos)

        print("Scan concluído! IPs salvos em lista_IPs.txt.")

    else:
        print("Erro: Gateway não encontrado no traceroute.")