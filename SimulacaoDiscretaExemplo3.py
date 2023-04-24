'''
    Neste exercicio registraremos além da chegadas e tamanho da fila, iremos registrar o tempo que aquela entidade ficou na fila.

    -> Considerações:
        . Taxa de chegada: 1 cliente por minuto
        . Taxa de atendimento: 2 clientes por minuto

        . Etapas de um processo:
            - Solicitar o servidor
            - Ocupar o servidor
            - Executar o atendimento
            - Liberar o servidor para o proximo cliente

'''

#Começamos a simulação importando as bibliotecas
import random       #Gerador de número aleatório
import simpy        #Biblioteca da simulação
import matplotlib.pyplot as plt

TEMPO_SIMULACAO = 480
TEMPO_MEDIO_CHEGADAS = 5
TEMPO_MEDIO_ATENDIMENTO = 10
TEMPO_ESPERA = []

#Criando a função que cria chegadas de entidades no sistema
def geraChegadas(env):
    contaChegada = 0

    while True:

        #Codigo fonte da chegada de entidades no sistema
        yield env.timeout(random.expovariate(1/TEMPO_MEDIO_CHEGADAS))
        contaChegada += 1

        env.process(atendimentoServidor(env, servidorRes))

#Criamos uma função para gerar a ocupação do servidor e realizar o atendimento
def atendimentoServidor(env, servidorRes):

    #Armazena o instante de chegada do cliente
    chegada= env.now

    #Solicita o servidor um recurso
    with servidorRes.request() as request:

        #Aguarda em fila até a liberação de espaço
        yield request

        #Calcula o tempo em fila pegando o momento de chegada até ser atendido
        tempopFila = env.now - chegada
        TEMPO_ESPERA.append(tempopFila)
        
        #Criando um tempo de atendimento
        yield env.timeout(random.expovariate(1.0/TEMPO_MEDIO_ATENDIMENTO))              #Aqui inicio o atendimento propriamento dito

#Fixando a semente geradora de número aleatórios
random.seed(1000)

#Criando o ambiente do modelo atual 
env = simpy.Environment()

#Criando o recurso servidorRes          
servidorRes = simpy.Resource(env, capacity= 1)  #Capacidade de atendimento simultaneos

#Inicia o processo de geração de chegadas
env.process(geraChegadas(env))

#Define por quanto tempo vai acontecer a simulação
env.run(until=TEMPO_SIMULACAO)

# Plotar o gráfico de dispersão dos tempos de espera
plt.scatter(range(len(TEMPO_ESPERA)), TEMPO_ESPERA, s=10)
plt.xlabel('Índice do Cliente')
plt.ylabel('Tempo de Espera (min)')
plt.title('Tempo de Espera por Cliente')
plt.show()