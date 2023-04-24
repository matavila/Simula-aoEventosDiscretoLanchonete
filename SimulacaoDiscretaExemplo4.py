'''
    Nesse exemplo temos uma sequência de atividades:
    - Condições da Lavanderia: 4 lavadoras, 3 secadoras e 5 cestos de roupas sujas
        -> Cliente chega e coloca a roupa para lavar (ou fica em fila)    
        -> Lavagem: 20min. 
        -> Ao fim da lavagem o cliente retira roupas da máquina, coloca num cesto.
        -> Leva o cesto até a secadora uniforme (1 a 4 min)
        -> Descarrega as roupas do cesto para a secadora
        -> Espera a secagem e vai embora (9 a 12 min)
    
    - Sequência de ocupação:
        . Cliente chega;
        . Ocupa a lavadora;
        . Lava;
        . Ocupa cesto;
        . Libera uma lavadora
        . Ocupa uma secadora
        . Libera cesto
        . Seca
        . Libera secadora

    Fatores a considerar :
        - Alteração na capacidade: Executar a simulação com diferentes valores de capacidade e gera efeitos na saida dos dados do modelo,
         Por exemplo, podemos executar a simulação com uma capacidade de 1 e, em seguida, executá-la novamente com uma capacidade de 2 e 
         comparar as taxas de ocupação do recurso. Se a taxa de ocupação for menor quando a capacidade é maior, isso sugere que a adição 
         de mais recursos melhora a operação.

        Outra maneira de verificar o efeito da alteração da capacidade é utilizar métricas de desempenho, como o tempo médio de espera na 
        fila ou o número médio de clientes na fila. Essas métricas podem ser comparadas entre diferentes valores de capacidade para avaliar
        o impacto da alteração.
    
'''

#Importando as bibliotecas necessárias
import random
import simpy
import matplotlib.pyplot as plt

tempoEsperaLavadora = []
#Função que armazena as distribuições de probabilidades utilizadas no modelo
def distribuicao(tipo):
    return {
        'chegada' : random.expovariate(1.0/5.0),
        'lavar' : 20,
        'carregar': random.uniform(1,4),
        'descarregar': random.uniform(1,2),
        'secar': random.uniform(9,12)
    }.get(tipo, 0.0)


#Função que gera a chegada de clientes
def chegadaClientes(env, lavadoras, cestos, secadoras):
    global contaClientes

    contaClientes = 0
    while True:
        contaClientes += 1

        yield env.timeout(distribuicao('chegada'))

        #Depois da chegada, iremos chamar o processo de lavagem ou secagem
        env.process(lavaSeca(env, lavadoras, cestos, secadoras))

#Função que processa a operação de cada cliente dentro da Lavanderia
def lavaSeca(env, lavadoras, cestos, secadoras):

    #Ocupa a Lavadora
    req1 = lavadoras.request()
    yield req1
    yield env.timeout(distribuicao('lavar'))

    #Ocupa um cesto enquanto está lavando lavadora
    req2 = cestos.request()
    yield req2
    yield env.timeout(distribuicao('carregar'))

    #Libera a lavadora, porém ainda permance com o cesto
    lavadoras.release(req1)

    #Ocupa a Secadora antes de liberar o cesto
    req3 = secadoras.request()
    yield req3
    yield env.timeout(distribuicao('descarregar'))

    #Libera o cesto mas não a lavadora
    cestos.release(req2)
    yield env.timeout(distribuicao('secar'))

    #Libera a secadora
    secadoras.release(req3)


#Semente fixa do gerador aleatório de dados
random.seed(10)

#Cria o ambiente de simulação
env = simpy.Environment()

#Recursos
lavadoras = simpy.Resource(env, capacity= 1)
cestos = simpy.Resource(env, capacity= 1)
secadoras = simpy.Resource(env, capacity=1)

'''
 Intuito: 
 Gráfico de linha -> da taxa de ocupação de cada recurso (lavadoras, cestos e secadoras) ao longo do tempo.
 Isso pode ajudar a identificar gargalos na operação e determinar se mais recursos são necessários.
'''

# Taxas de ocupação dos recursos
taxas_lavadoras = []
taxas_cestos = []
taxas_secadoras = []

# Função que atualiza as taxas de ocupação dos recursos e armazena em suas respectivas listas
def monitorarRecursos(env, lavadoras, cestos, secadoras, taxas_lavadoras, taxas_cestos, taxas_secadoras):
    while True:
        taxas_lavadoras.append(lavadoras.count / lavadoras.capacity)
        taxas_cestos.append(cestos.count / cestos.capacity)
        taxas_secadoras.append(secadoras.count / secadoras.capacity)
        yield env.timeout(1)



#Inicia o processo de geração de chegada
env.process(chegadaClientes(env, lavadoras, cestos, secadoras))

# Inicia o monitoramento das taxas de ocupação dos recursos
env.process(monitorarRecursos(env, lavadoras, cestos, secadoras, taxas_lavadoras, taxas_cestos, taxas_secadoras))

#Tempo de simulação
env.run(until=140)

# Gráfico de linha ->
tempo = range(len(taxas_lavadoras))
plt.plot(tempo, taxas_lavadoras, label="Lavadoras")
plt.plot(tempo, taxas_cestos, label="Cestos")
plt.plot(tempo, taxas_secadoras, label="Secadoras")
plt.title("Taxa de ocupação de recursos")
plt.xlabel("Tempo")
plt.ylabel("Taxa de ocupação")
plt.legend()
plt.show()

