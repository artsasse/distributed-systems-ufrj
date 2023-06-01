import socket

class Cliente:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None

    def conecta(self):
        '''Cria um socket de cliente e conecta-se ao servidor.'''
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Internet (IPv4 + TCP)
        self.sock.connect((self.host, self.port))

    def faz_requisicoes(self):
        '''Envia requisições para o servidor e exibe os resultados.'''
        # Lê mensagens do usuário até digitar 'fim'
        while True:
            msg = input("Digite uma mensagem ('fim' para terminar): ")
            if msg == 'fim':
                break

            # Envia a mensagem do usuário para o servidor
            self.sock.sendall(msg.encode('utf-8'))

            # Aguarda a resposta do servidor
            msg = self.sock.recv(1024)

            # Exibe a mensagem recebida
            print(str(msg, encoding='utf-8'))

        # Encerra a conexão
        self.sock.close()

    def executa(self):
        '''Método principal para executar o loop do cliente.'''
        self.conecta()
        self.faz_requisicoes()


if __name__ == '__main__':
    HOST = 'localhost'  # Máquina do servidor
    PORT = 10000        # Porta de escuta do servidor

    cliente = Cliente(HOST, PORT)
    cliente.executa()
 