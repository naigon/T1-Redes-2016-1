# comando para gerar certificado auto assinado e chave <openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -subj "/C=BR/ST=Rio Grande do Sul/L=Pelotas/O=UFPel/CN=localhost" -keyout ssl.key -out ssl.crt>

import _thread as thread
import time, socket, json, os, subprocess, ssl

HOST = 'localhost' # Endereco IP do Servidor(local)
PORT = 30000        # Porta que o Servidor esta

#inicializa no servidor com o arquivo json contendo usuarios cadastrados
arq = open('userlist.json','r')
lista = arq.read()
arq.close()
listajson = json.loads(lista)

#contexto SSL
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="ssl.crt", keyfile="ssl.key")

#cria socket normal
socket_servidor = socket.socket()
socket_servidor.bind((HOST, PORT))


#socket comeca a esperar conexao com limite maximo de 4 conexoes simultaneas
socket_servidor.listen(4)
print('\nEsperando Conexoes...\n')

#compara arquivo json do usuario com o de clientes cadastrados no servidor para efetuar a autentificacao
def autentica(user):
	userjson = json.loads(user)
	login = False
	
	for id in listajson['userlist']:
		if (id['usuario']==userjson['usuario'] and id['senha']==userjson['senha']):
			login = True
	
	return login

def trataCliente(connstream, endereco):
	print("Um cliente com o endereco: ", endereco," foi conectado!\n")
	log = False
	sair = False
	while sair == False:
		comando = connstream.recv(1024)
		comando = comando.decode()
		#COMANDO USER
		if comando == "user":
			
			connstream.send(b'1') 
			usuario = connstream.recv(1024)
			usuario = usuario.decode()
			if autentica(usuario) == True:
				log = True
				sucesso = b'100'
				#manda mensagem de sucesso pro cliente
				connstream.send(sucesso)
			else:
				erro = b'102'
				#manda mensagem de erro pro cliente
				connstream.send(erro)
		#COMANDO SEND
		elif comando == "send" and log == True:
			connstream.send(b'1')
			arq2= open("pipeServidor.js","wb")
			try:
				data = connstream.recv(2048)
				arq2.write(data)
				connstream.send(b"200")
			except connstream.error:
				connstream.send(b"201")
			arq2.close()
		#COMANDO RUN
		elif comando == "run" and log == True:	
			#executa codigo da aplicacao javascript com comando node (em algumas maquinas pode ser pelo comando nodejs)
			proc = subprocess.check_output(["node","pipeServidor.js","ulimit -m 512 -n 0"],timeout=10000)
			#envia resposta pro cliente
			connstream.send(b'305' + b' ' + b'Resposta: ' + proc)
		#COMANDO QUIT	
		elif comando == "quit" and log == True:
			sair = True
			connstream.send(b'1')
			paramquit = connstream.recv(2048)
			connstream.send(b"Conexao Encerrada")
			break
		else:
			if comando == "user" or comando == "send" or comando == "quit":
				connstream.send(b'1')
				inv = connstream.recv(2048)
			if comando == "quit": 
				connstream.send(b"Volte Sempre...")
				break
			connstream.send(b"Usuario nao Autentificado!\n")
	print("Cliente ",endereco," desconectado!\n")
	connstream.close()

def criaThreads_cliente():
    # Ouve processos ateh...
	while True:
		# Aceita uma conexao quando encontrada e devolve a
		# um novo socket conexao e o endereco do cliente
		# conectado
		conexao, endereco = socket_servidor.accept()
		#"envelopa" socket no contexto SSL
		connstream = context.wrap_socket(conexao, server_side=True,do_handshake_on_connect=True)
		# Inicia nova thread para lidar com o cliente
		thread.start_new_thread(trataCliente, (connstream, endereco))

criaThreads_cliente()
        
