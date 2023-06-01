import json
import threading

class Dicionario:
    
    def __init__(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo
        self.carregar()

    def carregar(self):
        '''Carrega o dicionário de um arquivo'''
        try:
            with open(self.nome_arquivo, 'r') as f:
                self.dicionario = json.load(f)
        except FileNotFoundError:
            print("ERRO: Dicionário não encontrado.")
            self.dicionario = {}

    def salvar(self):
        '''Salva o dicionário em um arquivo'''
        with open(self.nome_arquivo, 'w') as f:
            json.dump(self.dicionario, f)

    def adicionar(self, chave, valor):
        '''Adiciona um valor a uma chave do dicionário'''
        if chave in self.dicionario:
            self.dicionario[chave].append(valor)
        else:
          self.dicionario[chave] = [valor]
        self.salvar()
        print(f"Valor '{valor}' adicionado à chave '{chave}' com sucesso.")
        return self.dicionario[chave]

    def remover(self, chave):
        '''Remove uma chave do dicionário'''
        if chave in self.dicionario:
            del self.dicionario[chave]
            self.salvar()
            print("Chave removida com sucesso.")
        else:
            print("ERRO: Chave não encontrada.")

    def buscar(self, chave):
        '''Busca uma chave no dicionário'''
        print(f"Buscando chave '{chave}'...")
        if chave in self.dicionario:
            return self.dicionario[chave]
        else:
            return []