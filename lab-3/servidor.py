import rpyc
from rpyc.utils.server import ThreadedServer
from persistencia import Dicionario

class DicionarioService(rpyc.Service):
    def __init__(self):
        self.dicionario = Dicionario('dicionario.json')

    def on_connect(self, conn):
        print(f"Cliente conectado")
        
    def on_disconnect(self, conn):
        print(f"Cliente desconectado")

    def exposed_adicionar(self, chave, valor):
        return self.dicionario.adicionar(chave, valor)

    def exposed_buscar(self, chave):
        return self.dicionario.buscar(chave)

    def exposed_remover(self, chave):
        return self.dicionario.remover(chave)

if __name__ == "__main__":
    servidor = ThreadedServer(DicionarioService(), port=10000)
    print("Pronto para receber conexoes...")
    servidor.start()
