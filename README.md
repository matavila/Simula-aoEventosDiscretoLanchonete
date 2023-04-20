# Simulação de Eventos Discretos
Passo a passo para criar uma simulação por eventos discretos para uma lanchonete:

(1) Identifique o problema ou questão: identificar o problema que você está tentando resolver. Neste caso, o problema é como otimizar o fluxo de clientes em uma lanchonete, reduzindo o tempo de espera e melhorando a eficiência do atendimento.

(2) Identifique as variáveis e os parâmetros: As variáveis são os elementos que afetam o sistema e os parâmetros são valores que podem ser ajustados para controlar o comportamento da simulação. Algumas variáveis podem incluir o número de clientes que chegam à lanchonete, o tempo que cada cliente leva para fazer o pedido e o tempo que cada pedido leva para ser preparado. Alguns parâmetros podem incluir a capacidade de atendimento da lanchonete, o número de funcionários e o tempo de espera máximo permitido.

(3) Crie um modelo: Com base nas variáveis e parâmetros identificados, crie um modelo que represente o sistema da lanchonete. O modelo deve incluir as etapas do processo de atendimento ao cliente, como chegada, atendimento, preparação e pagamento. Também deve incluir regras para lidar com situações como filas de espera e capacidade máxima da lanchonete.
    - Chegada do cliente: Os clientes chegam à lanchonete em intervalos aleatórios, seguindo uma distribuição exponencial. Quando chegam, eles se juntam a uma fila de espera.

    - Atendimento do cliente: Quando um atendente estiver disponível, o próximo cliente da fila é atendido. O atendente leva um tempo aleatório para atender o cliente, seguindo uma distribuição normal. Durante o atendimento, o cliente faz seu pedido.

    - Preparação do pedido: Depois que o cliente faz o pedido, ele é encaminhado para a equipe de preparação. A equipe de preparação leva um tempo aleatório para preparar o pedido, seguindo uma distribuição normal.

    - Pagamento: Quando o pedido estiver pronto, o cliente faz o pagamento e deixa a lanchonete.

    - Saída do cliente: O cliente é removido do sistema após o pagamento.
    
(4) Execute a simulação: Depois que o modelo é codificado, execute a simulação e colete dados. Execute a simulação várias vezes com diferentes parâmetros para ver como diferentes cenários afetam o desempenho da lanchonete.

(5) Analise os resultados: Analise os dados coletados para ver como diferentes parâmetros afetam o desempenho da lanchonete. Identifique áreas que podem ser melhoradas e experimente com diferentes parâmetros para encontrar a melhor configuração para a lanchonete.

A razão pela qual cada passo é importante é que cada um contribui para a criação de uma simulação precisa e eficaz. Identificar o problema ajuda a garantir que a simulação esteja focada em resolver um problema real, enquanto a identificação de variáveis e parâmetros ajuda a garantir que a simulação seja personalizada para as necessidades específicas da lanchonete.
