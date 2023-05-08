# Laboratório 2 - Sistemas Distribuídos

## Arquitetura de Software

A arquitetura deste software é organizada em 3 **camadas**, de cima para baixo:

1. Interface com o Usuário
* Oferece uma interface de linha de comando, com apenas 3 tipos de comando, um para adicionar um novo par (chave, valor) no dicionário, o segundo para consultar o valor de uma chave e o último para adicionar mais um valor a uma chave existente. Todos esses comandos serão passados à camada 2, para que possa solicitar as respectivas modificações e leituras à camada de persistência dos dados.
2. Processamento das Requisições
* Carrega os dados persistidos obtidos da camada de Acesso, atualiza com os novos dados recebidos da Interface e pede para a camada 3 fazer a persistência novamente.
* Esta camada também será interativa e permitirá que o administrador ordene a exclusão de entradas persistidas na camada 3 ou o próprio fim da execução do servidor, se não houver mais clientes ativos.
3. Acesso e Persistência dos Dados
* Disponibiliza e atualiza os dados persistidos de acordo com os pedidos da camada 2.

De certa forma, a arquitetura também será **orientada a objetos**, já que cada camada corresponderá a um objeto que oferece uma interface com métodos e atributos para a camada acima.

## Arquitetura de Sistema

O sistema será dividido em Cliente e Servidor. Na parte do cliente, ficará a Interface com o Usuário, enquanto que as outras 2 camadas ficarão localizadas no servidor.

### Início do servidor

Assim que o servidor for iniciado, deve criar um arquivo para armazenar o novo dicionário e ficar na escuta para possíveis conexões de clientes.

### Início do cliente

A informação sobre porta e endereço do servidor estará pré-definida no código dos clientes. Assim que o cliente iniciar, vai tentar estabelecer conexão com o servidor e vai retornar uma mensagem para o usuário de acordo com o sucesso ou fracasso da sua tentativa. Ao obter sucesso, permitirá que o usuário utilize o terminal para escrever seus comandos.

### Troca de mensagens

O cliente pode enviar 2 tipos de mensagens para o servidor:

1. Uma string alfanumérica, correspondente à uma chave. Se a chave existir no dicionário, o servidor retorna a lista de valores associados, em ordem alfabética. Se a chave não existir, retorna uma lista vazia. 
* Ex: Cliente envia "chave". Servidor responde ["valor1", "valor2"].
* Ex: Cliente envia "chavi". Servidor responde [].

2. Dois termos alfanuméricos separados por vírgula como em "chave, valor". Se já existir uma chave com esse nome, o servidor acrescentará o novo valor à lista e responderá com a lista de valores atualizada. Se não existir, o servidor criará a chave no dicionário com o valor fornecido e retornará a nova lista, com apenas o valor fornecido inicialmente. 
* Ex. 1: Cliente envia ("chave1", "valor2"). Servidor responde ["valor1", "valor2"].
* Ex. 2: Cliente envia ("chave2", "valorX"). Servidor responde ["valorX"].

## Implementação 

O primeiro passo foi pegar o código multiplexado e concorrente visto nas vídeo-aulas e adaptá-lo para o objetivo deste trabalho.

Primeiramente, dividimos o código em 2 arquivos com nomes auto-explicativos: `cliente.py` e `servidor.py`.

Depois, criamoso o arquivo `persistencia.py` que abriga a classe Dicionario, que cuida da parte de acesso e persistência no arquivo que guarda os dados do dicionário.

Para fazer a persistência, decidimos salvar o dicionário em um arquivo JSON, que é atualizado a cada modificação solicitada pelo cliente.

Para evitar erros de race condition no acesso ao dicionário do Python e ao arquivo JSON, utilizamos um lock  em `servidor.py` toda vez que vamos utilizar algum método da classe Dicionario (com o context manager - with - tudo fica mais fácil e mais legível).





