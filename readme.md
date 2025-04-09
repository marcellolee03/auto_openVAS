# AutoVAS
AutoVAS é um projeto que visa automatizar todos os processos que levam à realização de um scan em uma rede local, desde a listagem de todos os hosts conectados ao gateway até a criação de uma planilha excel contendo os dados mais pertinentes do report. 

# Instalação
É possível instalar este pacote diretamente da fonte clonando o repositório Git:

	# Clonando repositório
	git clone https://github.com/marcellolee03/auto_openVAS.git
	
	# Instalando dependências
	sudo apt install python3-tk
	udo apt install traceroute
	sudo apt install nmap
	
**!!ATENÇÃO!!**
AutoVAS atualmente só é compatível com a GREENBONE-COMMUNITY-EDITION do OpenVAS utilizado em ambientes Linux!

# Utilizando AutoVAS
Ao abrir o programa pela primeira vez e a cada vez que reiniciar os contêineres do OpenVAS, deve-se colocar a senha sudo e clickar no botão escrito "Setup OpenVAS". Após o processo ser finalizado, basta preencher os campos "Senha do OPENVAS" e "Nome da TASK" e clickar em "Realizar Scan" para dar início ao processo!
