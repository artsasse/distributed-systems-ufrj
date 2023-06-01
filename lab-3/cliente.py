import rpyc

class Cliente:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port

    def conecta(self):
        self.conn = rpyc.connect(self.server_host, self.server_port)

    def help(self):
        print("\nInstruções:")
        print("- Para adicionar um valor a uma chave, digite: <chave>, <valor>")
        print("- Para buscar os valores de uma chave, digite: <chave>")
        print("- Para remover uma chave, digite: remover <chave>")
        print("- Para encerrar a conexão, digite: fim\n")

    def faz_requisicoes(self):
        self.help()
        while True:
            msg = input("Digite uma mensagem ('help' para comandos possíveis): ")
            if msg == 'fim':
                break
            elif msg == 'help':
                self.help()
            elif msg.startswith("remover"):
                chave = msg.split(" ")[1]
                resposta = self.conn.root.remover(chave)
                print(resposta)
            elif ',' in msg:
                chave, valor = msg.split(',')
                chave = chave.strip()
                valor = valor.strip()
                resposta = self.conn.root.adicionar(chave, valor)
                print(f"Adicionado com sucesso. A chave '{chave}' possui os valores: {resposta}.")
            else:
                chave = msg
                resposta = self.conn.root.buscar(chave)
                print(f"Os valores associados a chave '{chave}' são: {resposta}")

    def desconecta(self):
        self.conn.close()

    def executa(self):
        self.conecta()
        print(f"Conectado ao servidor: {self.server_host}:{self.server_port}")
        self.faz_requisicoes()
        self.desconecta()
        print(f"Desconectado do servidor: {self.server_host}:{self.server_port}")


if __name__ == "__main__":
    HOST = 'localhost'  
    PORT = 10000        

    cliente = Cliente(HOST, PORT)
    cliente.executa()
