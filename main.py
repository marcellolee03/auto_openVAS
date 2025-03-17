import subprocess
from re import search, MULTILINE

# Executando o traceroute e capturando a saída
saida_traceroute = subprocess.run("traceroute -n google.com", shell=True, capture_output=True, text=True)
saida_traceroute = saida_traceroute.stdout

# Pegando o primeiro IP da lista (Gateway)
match = search(r"^\s*1\s+([\d.]+)", saida_traceroute, MULTILINE)

if match:
    gateway_ip = match.group(1)
    print(f"Gateway encontrado: {gateway_ip}")

    # Comando Nmap para escanear a rede do Gateway
    comando_nmap = f"nmap -sP {gateway_ip}/24 | awk '/is up/ " + "{print up}; {gsub(/\\(|\\)/, \"\"); up = $NF}'"

    # Executando o Nmap e armazenando os IPs
    resultado = subprocess.run(comando_nmap, shell=True, capture_output=True, text=True)
    ips_ativos = resultado.stdout.strip()

    # Salvando os IPs no arquivo lista_IPs.txt
    with open("lista_IPs.txt", "w") as file:
        file.write(ips_ativos)

    print("Scan concluído! IPs salvos em lista_IPs.txt.")

else:
    print("Erro: Gateway não encontrado no traceroute.")