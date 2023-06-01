import json
import threading

class Dicionario:
    
    def __init__(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo
        self.lock = threading.Lock()
        self.carregar()

    def carregar(self):
        try:
            with open(self.nome_arquivo, 'r') as f:
                self.dicionario = json.load(f)
        except FileNotFoundError:
            print("ERRO: Dicionário não encontrado.")
            self.dicionario = {}

    def salvar(self):
        with open(self.nome_arquivo, 'w') as f:
            json.dump(self.dicionario, f)

    def adicionar(self, chave, valor):
        with self.lock:
            if chave in self.dicionario:
                self.dicionario[chave].append(valor)
                self.dicionario[chave].sort() 
            else:
                self.dicionario[chave] = [valor]
            self.salvar()
        print(f"Valor '{valor}' adicionado à chave '{chave}' com sucesso.")
        return self.dicionario[chave]

    def remover(self, chave):
        with self.lock:
            if chave in self.dicionario:
                del self.dicionario[chave]
                self.salvar()
                print("Chave removida com sucesso.")
                return "Chave removida com sucesso."
            else:
                print("ERRO: Chave não encontrada.")
                return "ERRO: Chave não encontrada."

    def buscar(self, chave):
        with self.lock:
            print(f"Buscando chave '{chave}'...")
            if chave in self.dicionario:
                return self.dicionario[chave]
            else:
                return []
