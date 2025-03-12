import subprocess
import re

#recebendo o ip do gateway e armazenando em uma variável
saida_traceroute = subprocess.run("traceroute google.com", shell = True, capture_output = True, text = True)
saida_traceroute = saida_traceroute.stdout

match =  re.search(r"_gateway \(([\d.]+)\)", saida_traceroute)
gateway_ip = match.group(1)

#montando a linha de comando
comando = f"nmap -sP {gateway_ip}/24 | awk '/is up/ " + "{print up}; {gsub(/\\(|\\)/, \"\"); up = $NF}'"

#armazenando a lista de IPs em um arquivo .txt
resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
resultado = resultado.stdout

with open("lista_IPs.txt", "w") as file:
    file.write(resultado)