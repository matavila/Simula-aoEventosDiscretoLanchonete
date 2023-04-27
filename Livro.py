'''
    Desafio 1: dois apostadores iniciam um jogo de cara ou coroa em que cada um deles aposta $1 sempre em um mesmo lado da moeda.
    O vencedor leva a aposta total ($2). Cada jogador tem inicialmente $10 disponíveis para apostar. O jogo termina quando um dos jogadores
    atinge a ruína e não tem mais dinheiro para apostar.
'''

#Importando a biblioteca
import random                   # gerador de números aleatórios

names = ['Chewbacca', 'R2D2']   # jogadores

def transfer(winner, looser, bankroll, tossCount):
    # função que transfere o dinheiro do winner para o looser
    # imprime o vencedor do lançamento  e o bankroll de cada jogador
    bankroll[winner] += 1
    bankroll[looser] -= 1
    print("\nLançamento: %d\tVencedor: %s" % (tossCount, names[winner]))
    print("%s possui: $%d e %s possui: $%d"
            % (names[0], bankroll[0], names[1], bankroll[1]))

def coinToss(bankroll, tossCount):
    # função que sorteia a moeda e chama a transfer
    if random.uniform(0, 1) < 0.5:
        transfer(1, 0, bankroll, tossCount)
    else:
        transfer(0, 1, bankroll, tossCount)

def run2Ruin(bankroll):
    # função que executa o jogo até a ruina de um dos jogadores
    tossCount = 0               # contador de lançamentos
    while bankroll[0] > 0 and bankroll[1] > 0:
        tossCount += 1
        coinToss(bankroll,tossCount)
    winner = bankroll[1] > bankroll[0]
    print("\n%s venceu depois de %d lançamentos, fim de jogo!"
            % (names[winner], tossCount))

bankroll = [5, 5]               # dinheiro disponível para cada jogador
#run2Ruin(bankroll)              # inicia o jogo



#===================================================================================================================================
'''
    Desafio -> Sua primeira missão será construir uma função que gere entidades com intervalos entre chegadas sucessivas exponencialmente distribuídos,
    com média de 2 min. Simule o sistema por 10 minutos apenas.
'''
#(1) Importando as bibliotecas
#import random
#import simpy

#(2) Definindo uma seed de chave aleatória para a biblioteca random
#random.seed(1000)

#(4) Criando um gerador de chegadas dentro do environment
'''
    Parâmetros de um processo (environment, entidade, taxa desejada)
'''
"""def geraChegadas(env, nome, taxa):
    contaChegada = 0
    while True:
        #Gerador de intervalo de chegadas
        '''
            Onde lambd é a taxa de ocorrência dos eventos ou, matematicamente, o inverso do tempo médio entre eventos sucessivos.
            No caso, se queremos que as chegadas ocorram entre intervalos médios de 2 min, a função ficaria:
        '''
        yield env.timeout(random.expovariate(1.0/taxa))    
        contaChegada += 1
        print(f"{nome} {contaChegada} chega em: {env.now:0.1f} ") 
"""

#(3) Criando um environment
#env = simpy.Environment()

#(5) Criando o processo dentro do environment
#env.process(geraChegadas(env, "Cliente", 2))

#(6) Executamos o modelo
#env.run(until=10)


#===================================================================================================================================
'''
    Desafio -> A fila M/M/1 representa um sistema simples em que clientes chegam para atendimento em um servidor de fila única, com 
    intervalos entre chegadas sucessivas exponencialmente distribuídos e tempos de atendimentos também exponencialmente distribuídos.

    Precisamos, portanto, construir uma nova função que realize o processo de atendimento. Usualmente, um processo qualquer tem ao menos as 4 etapas a seguir:
        . Solicitar o servidor;
        . Ocupar o servidor;
        . Executar o atendimento por um tempo com distribuição conhecida;
        . Liberar o servidor para o próximo cliente.
'''
"""#(1) Importando as bibliotecas
import random
import simpy

#(2) Definindo uma seed fixa para chave aleatoria da biblioteca randon
random.seed(1000)




#(5) Definindo as variáveis
LIMITE_MAXIMO = 10
TEMPO_MEDIO_CHEGADA = 5
TEMPO_MEDIO_ATENDIMENTO = 3

#(4) Criando um gerador de chegadas com limitação de numero máximo de entidades
def geraChegada(env, nome, taxa):
    contachegada = 0                        #Fazendo a contagem de entidades que chegam
    while (contachegada < LIMITE_MAXIMO):

        #Gerando um evento de chegada de entidades no local
        yield env.timeout(random.expovariate(1/taxa))
        contachegada+=1                     #Incrementando a contagem a partir do momento que chega mais uma

        print(f"{nome} {contachegada} chega em: {env.now:0.1f} ") 

        #(14) Chamando o proximo evento, aquele depois da chegada do cliente
        env.process(atendimento(env, f"cliente {contachegada}", servidorRes))

#(9) Criando um evento de atendimento (ocupação de um servidor)
def atendimento (env, nome, servidorRecurso):

     #(16) Armazena o instante de chegada do cliente
    chegada = env.now 

    #(10) Solicitando a ocupação (entra na fila)
    request = servidorRecurso.request() 

    #(11) Aguarda em fila até a liberação e ocupa 
    yield request
    #(16) Armazena o instante de chegada do cliente
    tempofila = env.now - chegada
    print(f'{env.now:0.1f} Servidor inicia o atendimento do {nome} \t Tempo espera: {tempofila:0.1f}')

    #(12) Aguarda um tempo de atendimento exponencialmente distribuído (processo de atendimento)
    yield env.timeout(random.expovariate(1.0/TEMPO_MEDIO_ATENDIMENTO))
    print(f'{env.now:0.1f} Servidor termina o atendimento do {nome} \t Clientes em fila: {len(servidorRes.queue)}')

    #(13) Libera o recurso servidorRes (processo pós atendimento)
    yield servidorRes.release(request)
    print("===================") 

#(3) Criando um environment
env = simpy.Environment()

#(8) Criando um serviço ou recurso
servidorRes = simpy.Resource(env, capacity= 1)

#(6) Criando um processo no environment
env.process(geraChegada(env,"Cliente", TEMPO_MEDIO_CHEGADA))

#(7)Executando o modelo
#env.run(until=480)

#(15) Imprimindo o tempo de simulaçao e o número de clientes na fila
'''
    Para fazermos isso, basta lembrarmos que a qualquer momento, o conjunto de entidades
    em fila pelo recurso é dado por servidorRes.queue e, portanto, o número de entidade em fila é facilmente obtido pela expressão:
        - > len(servidorRes.queue)
'''


#(16) Imprimindo o tempo de permanência em fila de cada cliente.
'''
    calcule o tempo de permanência em fila de cada cliente e imprima o resultado na tela. Para isso, armazene o instante de chegada do
    cliente na fila em uma variável chegada. Ao final do atendimento, armazene o tempo de fila, numa variável tempoFila e apresente o
    resultado na tela.
'''"""

#https://simpy.livrosimulacao.eng.br/parte-i-introducao/criando-_ocupando_e_desocupando_recursos/exemplo_fila_mm1
#https://matplotlib.org/stable/tutorials/introductory/quick_start.html


#===================================================================================================================================
'''
    um problema clássico de simulação envolve ocupar e desocupar recursos na seqüência correta. Considere uma lavanderia com 4 lavadoras,
    3 secadoras e 5 cestos de roupas. Quando um cliente chega, ele coloca as roupas em uma máquina de lavar (ou aguarda em fila). A lavagem
    consome 20 minutos (constante). Ao terminar a lavagem, o cliente retira as roupas da máquina e coloca em um cesto e leva o cesto com suas
    roupas até a secadora, num processo que leva de 1 a 4 minutos distribuídos uniformemente. O cliente então descarrega as roupas do cesto 
    diretamente para a secadora, espera a secagem e vai embora. Esse processo leva entre 9 e 12 minutos, uniformemente distribuídos. Construa
    um modelo que represente o sistema descrito.
'''
"""#(1) Importando as bibliotecas
import random
import simpy
import matplotlib.pyplot as plt

#(16) Criando um armazenamento de tempo
Tempo = []
Clientes = []

#(2) Fixando a semente de aleatoriedade da biblioteca randon
random.seed(1000)

#(5) Criando um dicionário com etapa e tempo
def distribuição(tipo):
    return {
        'chegadas': random.expovariate(1.0/5.0),                #Desta forma o tempo médio de chegada é de 5min por cliente
        'lavar': 20,
        'carregar': random.uniform(1, 4),
        'descarregar': random.uniform(1, 2),
        'secar': random.uniform(9, 12),
    }.get(tipo, 0.0)

#(4) Criando um gerador de chegadas
def geraChegadas(env, lavadoras, secadoras, cestos):
    global contaClientes                                        #Transformando a variável expessifica em global
    contaClientes = 0

    while contaClientes < 10:

        #Gerando um evento de chegada de entidades no local
        contaClientes+= 1
        Clientes.append(contaClientes)
        yield env.timeout(distribuição('chegadas'))
        print(f'No minuto: {env.now:0.1f} chega o cliente {contaClientes}')

        # A partir do momento que o cliente chega, ele irá para o processo de ocupação dos recursos
        env.process(lavaSeca(env,f'Cliente {contaClientes}', lavadoras, secadoras, cestos))

#(6) Criando uma função de ocupação de recursos dentro da lavanderia 
def lavaSeca(env, nome, lavadoras, secadoras, cestos):
    
    chegada = env.now 

    #(7) Ocupando o recurso da lavadora
    Recurso1 = lavadoras.request()                             #Faz a solicitação da ocupação do recurso
    yield Recurso1                                             #Ocupa o recurso 
    print(f'No instante: {env.now:0.1f} o cliente {nome} ocupa a Lavadora \t Clientes em fila: {len(lavadoras.queue)}')
    yield env.timeout(distribuição('lavar'))                   #Chamamos a operação de lavagem que demora 20min

    #(8) Ocupação do cesto (que deve ser feito logo em seguida da ocupação da lavadora)
    Recurso2 = cestos.request()                                #Faz a solicitação da ocupação do recurso cesto
    yield Recurso2                                             #Ocupa o recurso
    print(f"No instante: {env.now:0.1f} o cliente {nome} ocupa o cesto \t Clientes em fila: {len(cestos.queue)}")
    yield env.timeout(distribuição('carregar'))                #Chama a operação da ocupação do cesto
    
    #(9) Finalização do processo de lavagem
    lavadoras.release(Recurso1)                                        #Faz a liberação do recurso Lavadora
    print(f"No instante {env.now:0.1f} O cliente {nome} desocupa a Lavadeira")

    #(10) Inicio da ocupação do processo de secagem
    Recurso3 = secadoras.request()                             #Faz a solicitação da ocupação do recurso secadora
    yield Recurso3                                             #Ocupa o recurso 
    print(f"No instante {env.now:0.1f} O cliente {nome} ocupa a Secadora \t Clientes em fila: {len(secadoras.queue)}")
    yield env.timeout(distribuição('descarregar'))             #Chama a operação de tirar a roupa da lavadeira e colocar no cesto

    #(11) Desocupação do cesto
    cestos.release(Recurso2)                                           #Faz a liberação do recurso Cesto
    print(f"No instante {env.now:0.1f} O cliente {nome} desocupa o Cesto")
    yield env.timeout(distribuição('secar'))                   #Inicia o processo de Secagem

    #(12) Desocupação da Secagem
    secadoras.release(Recurso3)
    print(f"No instante {env.now:0.1f} O cliente {nome} desocupa a Secadora")
    Tempototal= env.now - chegada
    Tempo.append(Tempototal)

#(3) Criando um environment(ambiente)
env= simpy.Environment()

#(13) Criação dos recursos
lavadoras = simpy.Resource(env, capacity=3)
cestos = simpy.Resource(env, capacity=2)
secadoras = simpy.Resource(env, capacity=1)

#(14) Criando o processo no ambiente
env.process(geraChegadas(env, lavadoras, cestos, secadoras))

#(15) Começa o processo
env.run(until=480)

#(17) Gera o gráfico de barras
labels = contaClientes
plt.bar(Clientes, Tempo)
plt.title('Tempo gasto por clientes')
plt.ylabel('Tempo')
plt.show()
"""
#===================================================================================================================================
'''
    Qual a diferença entre atributo e variável para um modelo de simulação? 
    O atributo pertence à entidade, enquanto a variável pertence ao modelo. De outro modo, se um cliente chega a uma loja e compra 1, 2
    ou 3 produtos, esse cliente possui um atributo imediato: o número de produtos comprados. Note que o atributo "número de produtos" é
    um valor diferente para cada cliente, ou seja: é um valor exclusivo do cliente.

    Por outro lado, um parâmetro de saída importante seria o número total de produtos vendidos nesta loja ao longo da duração da simulação.
    O total de produtos é a soma dos atributos "número de produtos" de cada cliente que comprou algo na loja. Assim, o total vendido é uma 
    variável do modelo, que se acumula a cada nova compra, independentemente de quem é o cliente.
'''
#(1) Importando as bibliotecas
import simpy
import random
import matplotlib.pyplot as plt

#(2) Definindo uma chave fixa para a biblioteca randon
random.seed(1000)

#(5) Criando uma variável global para marcar o número de vendas realizadas
contaVendas = 0
Clientes = []
ProdutosB = []

#(4) Criando uma função para gerar chegadas
def geraChegadas(env):
    # variável local = atributo da entidade: contaCliente e Produtos
    contaCliente = 0

    while contaCliente < 5:
        yield env.timeout(1)
        contaCliente += 1
        Clientes.append(contaCliente)

        # atributo do cliente: número de produtos desejados
        produtos = random.randint(1,3) 
        print(f"Instante: {env.now:0.1f} -> Chegada do cliente {contaCliente} \tProdutos desejados:{produtos}")

        # inicia o processo de atendimento do cliente de atributos contaEntidade
        # e do número de produtos
        env.process(Compras(env, f"cliente {contaCliente}", produtos))

# (5) função que realiza a venda para as entidades
def Compras(env, cliente, produtos):
    global contaVendas # variável global = variável do modelo

    # A linha for i in range(0, produtos): cria um loop que irá se repetir um número de vezes igual à quantidade 
    # de produtos que a entidade deseja comprar.
    for i in range(0, produtos):
        yield env.timeout(2)
        contaVendas += produtos
        print(f" Instante: {env.now:0.1f} -> Compra do {cliente} \tProdutos comprados: {produtos}")
    ProdutosB.append(contaVendas)
    
#(3) Criando um ambiente para a simulação
env = simpy.Environment()

#(4) Criando a simulação
env.process(geraChegadas(env))

#(6) Processando a simulação
env.run(until=480)                # roda a simulação por 10 unidades de tempo
print(f"\nTotal vendido:{contaVendas}produtos")

#(7) Gera o gráfico de barras
plt.bar(Clientes, ProdutosB)
plt.title('Compras por cliente')
plt.ylabel('Compras')
plt.show()