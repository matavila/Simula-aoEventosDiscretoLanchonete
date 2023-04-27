'''

 Gráfico de barras do número médio de clientes em espera na fila para cada recurso ao longo do tempo.
 Isso pode ajudar a identificar quais recursos têm filas mais longas e onde é necessário dedicar mais atenção.
'''

import simpy
import random
import matplotlib.pyplot as plt

# Função para gerar intervalo de tempo entre chegadas de clientes
def gera_intervalo_chegadas():
    return random.expovariate(1/5)

# Função para gerar o tempo de atendimento de um cliente
def gera_tempo_atendimento():
    return random.uniform(2, 5)

# Função para simular a operação de um cliente
def cliente(env, id, lavadoras, cestos, secadoras, tempo_espera, tempo_atendimento):
    # Cliente chega e espera por uma lavadora disponível
    chegada = env.now
    with lavadoras.request() as req:
        yield req
        espera = env.now - chegada
        tempo_espera.append(espera)

        # Cliente pega um cesto e aguarda sua vez na fila para usar a lavadora
        with cestos.request() as req2:
            yield req2
            # Cliente utiliza a lavadora por um tempo determinado
            yield env.timeout(tempo_atendimento)
        
        # Após lavar, o cliente espera por uma secadora disponível
        with secadoras.request() as req3:
            yield req3
            # Cliente utiliza a secadora por um tempo determinado
            yield env.timeout(gera_tempo_atendimento())

# Função para monitorar as filas de espera dos recursos
def monitorarFilas(env, lavadoras, cestos, secadoras, filas_lavadoras, filas_cestos, filas_secadoras):
    while True:
        filas_lavadoras.append(len(lavadoras.queue))
        filas_cestos.append(len(cestos.queue))
        filas_secadoras.append(len(secadoras.queue))
        yield env.timeout(1)

# Cria ambiente de simulação
env = simpy.Environment()

# Recursos
lavadoras = simpy.Resource(env, capacity=1)
cestos = simpy.Resource(env, capacity=1)
secadoras = simpy.Resource(env, capacity=1)

# Listas para armazenar os tempos de espera dos clientes e as filas de espera dos recursos
tempos_espera = []
filas_lavadoras = []
filas_cestos = []
filas_secadoras = []

# Inicia o monitoramento das filas de espera dos recursos
env.process(monitorarFilas(env, lavadoras, cestos, secadoras, filas_lavadoras, filas_cestos, filas_secadoras))

# Cria 10 clientes
for i in range(10):
    env.process(cliente(env, i, lavadoras, cestos, secadoras, tempos_espera, gera_tempo_atendimento()))

# Roda a simulação
env.run(until=30)

# Calcula o número médio de clientes em espera para cada recurso
media_lavadoras = sum(filas_lavadoras) / len(filas_lavadoras)
media_cestos = sum(filas_cestos) / len(filas_cestos)
media_secadoras = sum(filas_secadoras) / len(filas_secadoras)

# Gera o gráfico de barras
labels = ['Lavadoras', 'Cestos', 'Secadoras']
medias = [media_lavadoras, media_cestos, media_secadoras]
plt.bar(labels, medias)
plt.title('Número médio de clientes em espera por recurso')
plt.ylabel('Número médio de clientes')
plt.show()
