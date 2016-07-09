import socket, ssl

class Cliente(object):
	def __init__(self, server, port):
		
        # Servidor a ser conectado
		self.server = server
        # Port para ser usada
		self.port = port

		#contexto SSL
		context = ssl.create_default_context()
		context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
		context.verify_mode = ssl.CERT_REQUIRED
		context.check_hostname = True
		context.load_verify_locations("ssl.crt")
		#socket seguro
		sslSocket = context.wrap_socket(socket.socket(socket.AF_INET),server_hostname=self.server,do_handshake_on_connect=True)
		#conecta com o servidor
		
		if sslSocket.connect_ex((self.server, self.port)):
			print('\nreturn 101\n')#erro ao conectar(servidor offline)
		else:
			print('\nConectado com sucesso a (Servidor, Porta) : ' + str(sslSocket.getpeername()) + '\n')
			print('Lista de comandos:\n\n' + '\tuser <arquivo.json>\n' + '\tsend <arquivo.js>\n' + '\trun\n' + '\tquit <parametro>\n' )
						
			while True:
   			#recebe comandos pelo terminal
				cmd = input()
				cmd = cmd.split()
				
				if cmd[0] != 'user' and cmd[0] != 'send' and cmd[0] != 'run' and cmd[0] != 'quit':
					print('\nreturn Comando Invalido!\n')
					break
					
				if cmd[0] == 'user' or cmd[0] == 'send':
					arquivo = open(cmd[1],'r')
					parametro = arquivo.read()
				#manda comando
				sslSocket.send(cmd[0].encode())
				if cmd[0]!='run':
					manda = sslSocket.recv(2048)
					manda = manda.decode()
					if manda == '1' and cmd[0] != 'quit':
						sslSocket.send(parametro.encode())
					if manda == '1' and cmd[0] == 'quit':
						sslSocket.send(cmd[1].encode())
				#pega a resposta sobre a autentificacao do usuario
				resp1 = sslSocket.recv(1024)
				resp1 = resp1.decode()
				print ('\nreturn ',resp1,'\n')
					
				if cmd[0] == 'quit': break
			#fecha conexao
			sslSocket.close()
			
#ENDERECO E PORTA DO SERVIDOR
HOST = input("\nPor Favor, Digite o Endereço IP do Servidor: ")
PORTA = 30000

Cliente(HOST, PORTA)
