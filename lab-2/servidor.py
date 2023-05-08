# servidor de echo: lado servidor
# com finalizacao do lado do servidor
# com multithreading (usa join para esperar as threads terminarem apos digitar 'fim' no servidor)
import socket
import select
import sys
import threading
import re
from persistencia import Dicionario

# define a localizacao do servidor
HOST = ""  # vazio indica que podera receber requisicoes a partir de qq interface de rede da maquina
PORT = 10000  # porta de acesso

class Servidor:
    def __init__(self):
        """Cria um socket de servidor e o coloca em modo de espera por conexoes. Também cria um objeto do tipo Dicionario,
        um historico de conexões e uma lista de entradas para o Select."""

        # define a lista de I/O de interesse (já inclui a entrada padrão)
        self.entradas = [sys.stdin]

        # armazena historico de conexoes
        self.conexoes = {}

        # instancia o dicionario
        self.dicionario = Dicionario("dicionario.json")

        # cria lock para acesso ao dicionario
        self.lock = threading.Lock()

        # cria o socket
        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )  # Internet( IPv4 + TCP)

        # vincula a localizacao do servidor
        self.sock.bind((HOST, PORT))

        # coloca-se em modo de espera por conexoes
        self.sock.listen(5)

        # configura o socket para o modo nao-bloqueante
        # self.sock.setblocking(False)

        # inclui o socket principal na lista de entradas de interesse
        self.entradas.append(self.sock)

    def aceita_conexao(self):
        """Aceita o pedido de conexao de um cliente
        Entrada: o socket do servidor
        Saida: o novo socket da conexao e o endereco do cliente"""

        # estabelece conexao com o proximo cliente
        clisock, endr = self.sock.accept()

        # registra a nova conexao
        self.conexoes[clisock] = endr

        return clisock, endr

    def atende_requisicoes(self, clisock, endr):
        """Recebe mensagens e as envia de volta para o cliente (ate o cliente finalizar)
        Entrada: socket da conexao e endereco do cliente
        Saida:"""

        while True:
            # recebe dados do cliente
            data = clisock.recv(1024)
            if not data:  # dados vazios: cliente encerrou
                print(str(endr) + "-> encerrou")
                clisock.close()  # encerra a conexao com o cliente
                return

            # decodifica mensagem recebida
            msg = str(data, encoding="utf-8")
            print(str(endr) + ": " + msg)

            # Se tiver recebido uma tupla (chave, valor), adiciona ao dicionario
            if ',' in msg:
                chave, valor = msg.split(',')
                # Remove espaços em branco
                chave = chave.strip()
                valor = valor.strip()
                with self.lock:
                    valores_salvos = self.dicionario.adicionar(chave, valor)
                response = bytes(
                    f"Adicionado com sucesso. A chave '{chave}' possui os valores: {valores_salvos}.",
                    encoding="utf-8",
                )
            # Se tiver recebido apenas uma chave, retorna os valores associados a ela
            else:
                chave = msg
                with self.lock:
                    valores = self.dicionario.buscar(chave)
                response = bytes(
                    f"Os valores associados a chave '{chave}' são: {valores}",
                    encoding="utf-8",
                )

            clisock.sendall(response)  # envia a resposta para o cliente


    def executa(self):
        """Inicializa e implementa o loop principal (infinito) do servidor"""
        clientes = []  # armazena as threads criadas para fazer join
        print("Pronto para receber conexoes...")
        while True:
            # espera por qualquer entrada de interesse
            leitura, escrita, excecao = select.select(self.entradas, [], [])
            # tratar todas as entradas prontas
            for pronto in leitura:
                if pronto == self.sock:  # pedido novo de conexao
                    clisock, endr = self.aceita_conexao()
                    print("Conectado com: ", endr)
                    # cria nova thread para atender o cliente
                    cliente = threading.Thread(
                        target=self.atende_requisicoes, args=(clisock, endr)
                    )
                    cliente.start()
                    # armazena a referencia da thread para usar com join()
                    clientes.append(cliente)  
                elif pronto == sys.stdin:  # entrada padrao
                    cmd = input()
                    if cmd == "fim":  # solicitacao de finalizacao do servidor
                        for c in clientes:  # aguarda todas as threads terminarem
                            c.join()
                        self.sock.close()
                        sys.exit()
                    elif cmd == "hist":  # outro exemplo de comando para o servidor
                        print(str(self.conexoes.values()))
                    elif cmd.startswith("remover"):  # remover chave do dicionario
                        chave = cmd.split(" ")[1]
                        with self.lock:
                            self.dicionario.remover(chave)

if __name__ == "__main__":
    servidor = Servidor()
    servidor.executa()
