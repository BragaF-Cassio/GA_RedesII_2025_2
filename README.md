# Trabalho de Grau A: Redes de Computadores: Internetworking, Roteamento e Transmissão

## Professor:
- Cristiano Bonato Both

## Integrantes:
- Vicenzo Milan Maldaner
- Gabriel Cezar Walber
- Cássio Ferreira Braga

## Protocolo de roteamento por latência:
- Colunas da tabela de conhecimento
    - Identificador da rede
    - Roteador que devo enviar a informação (próximo hop)
    - Latência até a rede da topologia (tempo para chegar na rede)

### Tratamento com vizinhos
- Se for detectada que a conexão com um vizinho for perdida (timeout de tempo de recebimento de tabela):
    - Coloca um tempo alto na latência para aquela rota e rotas dependentes da mesma, e começa a propagar, para que outras rotas propaguem melhores caminhos, caso conheçam.

- Latência do recebimento da tabela do vizinho
    - Usada para somar ao tempo da tabela, para ter um valor próximo ao tempo real de envio.

### Envio e recebimento de tabelas
- Ao enviar tabela:
    - Envia tabela sem as rotas que passam pela rota ao qual a tabela está sendo enviada.

- Ao receber tabela:
    - Compara com os registros da tabela interna que passam pela rota que enviou a tabela, e obrigatoriamente atualiza os campos (pois o melhor caminho conhecido é esse, deve estar sempre atualizado.)
        - Se houver um registro que não existe na tabela recebida, mas existe na tabela interna, esse campo é somado com o tempo desde o último recebimento de tabela dessa rota.
    - Restante dos campos compara para ver se está melhor do que o que está atualmente registrado.

## Variáveis utilizadas:
- Tabela de registros (lista de struct)
    - Destino Rede (Identificador da Rede, variável/struct)
    - NextHop (IP, variável/struct)
    - Latência (ms, inteiro long sem sinal)

- Tabela de vizinhos (lista de struct)
    - Timestamp de envio para vizinho (ms, inteiro long sem sinal)
    - P (tempo em ms, inteiro sem sinal)
    - Delay da última informação recebida
