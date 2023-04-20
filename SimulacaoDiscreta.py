'''
    (1) Primeiro passo é a instalação da biblioteca Simpy, Randon e alguma biblioteca gráfica

    (2) Criação de uma função para geração de entidades

'''

#Importando o Simpy que serve para implementar o modelo de Simulação de Eventos Discretos
import simpy

'''#Importando o Random para que possamos gerar números aleatórios para basearmos o exemplo
import random'''

#Criando uma biblioteca de distribuição de tempo
def distribuicao(tipo):
    return {
        'FeSiAl' : 32,
        'Tial' : 25,
        'Desoxidante' : 10,
    }.get(tipo, 0.0)            #Pega o tempo em função do tipo, se não houver vai ser 0


# Função que define o processo da chegada
def geraChegadas(env, nome, limiteproducao):
    print(f"Produto {nome} chega ao processo em {env.now}")

    contaChegada = 0
    #Traz o tempo gasto para chegar cada produto
    taxa = distribuicao(nome)
    #Função que cria chegadas de entidades no sistema
    while contaChegada < limiteproducao:

        #Definindo o tempo do próximo evento
        yield env.timeout(taxa)
        contaChegada = contaChegada + 1 
        
        print(f" O produto {nome}, de posição {contaChegada} chega em {env.now:0.1f}")

#random.seed(1000)   #Semente geradora de número aleatório (fixando eles)
#Criando o ambiente do modelo na variável env
env = simpy.Environment()

#Criando o processo que chama a função de geração de chegadas
#Aderindo a colocação de um limitador de quantidade de produtos que podem chegar
env.process(geraChegadas(env, "FeSiAl",12))

env.run()
'''#Define o tempo da simulação
env.run(until=10)
'''




'''# Aguarda até que o caixa esteja livre
        yield req
        print(f"Produto {nome} começa a ser processado em {env.now}")

        # Tempo de processamento
        yield env.timeout(10)  
        print(f"Produto {nome} finaliza o processamento em {env.now}")

# Função que define o processamento do produto
def processo(env):
    while True:
        print(f"Processo começa a funcionar em {env.now}")
        yield env.timeout(50)  # Tempo de trabalho
        print(f"Processo encerra o funcionamento em {env.now}")

# Configuração da simulação
env = simpy.Environment()
equipamento = simpy.Resource(env, capacity=1)  # Capacidade do caixa

# Criação de eventos iniciais
env.process(processo(env))
env.process(geraChegadas(env, "A", equipamento))
env.process(geraChegadas(env, "B", equipamento))
env.process(geraChegadas(env, "C", equipamento))

# Inicia a simulação
env.run(until=10)  # Duração da simulação

'''
