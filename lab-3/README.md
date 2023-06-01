# Laboratório 3 - Sistemas Distribuídos - Aplicação RPC

## Arquitetura de Software

A arquitetura deste software é organizada em 3 **camadas**, de cima para baixo:

1. Interface com o Usuário
* Oferece uma interface de linha de comando com quatro tipos de comandos: adicionar um novo par (chave, valor) no dicionário, consultar o valor de uma chave, remover uma chave e terminar a conexão. Todos esses comandos serão passados à segunda camada, que solicitará as respectivas modificações e leituras da camada de persistência de dados.

2. Processamento das Requisições
* Esta camada carrega os dados persistidos obtidos da camada de Acesso, atualiza-os com os novos dados recebidos da Interface e pede para a camada 3 fazer a persistência novamente.

3. Acesso e Persistência dos Dados
* Disponibiliza e atualiza os dados persistidos de acordo com os pedidos da camada 2.

Semelhante à arquitetura anterior (sockets), este software também é **orientado a objetos**, já que cada camada corresponderá a um objeto que oferece uma interface com métodos e atributos para a camada acima.

## Arquitetura de Sistema

O sistema está dividido em Cliente e Servidor. A parte do cliente compreende a Interface com o Usuário, enquanto que as outras 2 camadas estão localizadas no servidor.

### Início do servidor

Assim que o servidor for iniciado, deve carregar o dicionário do arquivo e ficar na escuta para possíveis conexões de clientes.

### Início do cliente

A informação sobre porta e endereço do servidor está pré-definida no código dos clientes. Assim que o cliente iniciar, vai tentar estabelecer conexão com o servidor e vai retornar uma mensagem para o usuário de acordo com o sucesso ou fracasso da sua tentativa. Ao obter sucesso, permitirá que o usuário utilize o terminal para escrever seus comandos.

### Troca de mensagens

O cliente pode enviar 3 tipos de mensagens para o servidor:

1. Uma string alfanumérica, correspondente à uma chave. Se a chave existir no dicionário, o servidor retorna a lista de valores associados, em ordem alfabética. Se a chave não existir, retorna uma lista vazia. 

2. Dois termos alfanuméricos separados por vírgula, como em "chave, valor". Se já existir uma chave com esse nome, o servidor acrescentará o novo valor à lista e responderá com a lista de valores atualizada. Se não existir, o servidor criará a chave no dicionário com o valor fornecido e retornará a nova lista, com apenas o valor fornecido inicialmente.

3. Uma mensagem com a palavra "remover" seguida de uma chave. O servidor irá remover a chave especificada e retornará uma mensagem de sucesso ou falha.

## Implementação 

O primeiro passo foi alterar o código anterior para usar a biblioteca rpyc e adaptá-lo para o objetivo deste trabalho.

Primeiramente, mantivemos a divisão em 3 arquivos

 com nomes auto-explicativos: `cliente.py`, `servidor.py` e `persistencia.py`.

O arquivo `persistencia.py` abriga a classe Dicionario, que cuida da parte de acesso e persistência no arquivo que guarda os dados do dicionário.

Para fazer a persistência, decidimos salvar o dicionário em um arquivo JSON, que é atualizado a cada modificação solicitada pelo cliente.

Para evitar erros de condição de corrida no acesso ao dicionário do Python e ao arquivo JSON, utilizamos um lock em `persistencia.py` toda vez que vamos utilizar algum método da classe Dicionario. Com o gerenciador de contexto - with - tudo fica mais fácil e mais legível. Percebendo a tendência de que os arquivos de servidor e cliente se modifiquem com mais frequência que o
de persistência, achamos melhor guardar a lógica do lock junto com o próprio Dicionário, mudando a abordagem em relação ao último trabalho.




