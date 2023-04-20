#Importando o Simpy que serve para implementar o modelo de Simulação de Eventos Discretos
import simpy

#Definindo tempo médios de chegadas
Tempo_Medio_Chegada = 30
Tempo_Medio_Processamento = 120


# Função que define o processo da chegada
def geraChegadas(env):
    print(f"Produto chega ao processo em {env.now}")
    contaChegada = 0

    #Função que cria chegadas de entidades no sistema
    while True:

        #Definindo o tempo do próximo evento
        yield env.timeout(Tempo_Medio_Chegada)
        contaChegada = contaChegada + 1 
        print(f" O produto de posição {contaChegada} chega em {env.now:0.1f}")

        env.process(fabricacao(env, f"Produto numero {contaChegada}", processamento))

#Função que ocupa o equipamento e realiza o processo
def fabricacao(env, nome, processamento):
    with processamento.request() as request:
            
            #Gerando um aguardo em fila até a liberação do recurso e ocupa
            yield request

            #Recurso liberado para ir pro processamento
            print(f"Equipamento {env.now} inicia o processamento do {nome}")

            #Tempo que o recurso está em processo
            yield env.timeout(Tempo_Medio_Processamento)
            

#Criando o ambiente do modelo na variável env
env = simpy.Environment()

#Criando o recurso de fabricação
processamento = simpy.Resource(env, capacity=1)

#Criando o processo que chama a função de geração de chegadas
env.process(geraChegadas(env))

env.run(until=12)