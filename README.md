# Projeto: Playground de RabbitMQ 🐰

> Este repositório é um ambiente de testes interativo criado para o time de estagiários. O objetivo é "brincar" com os conceitos do RabbitMQ de forma prática e segura.

## 👋 Olá, Time!

Sejam bem-vindos! Este projeto foi criado pensando em vocês. A melhor forma de aprender uma tecnologia como o RabbitMQ é vendo ela funcionar, quebrando e consertando. E é exatamente isso que vamos fazer aqui.

Sintam-se à vontade para clonar, modificar, testar e quebrar tudo. A ideia é que vocês usem este espaço para solidificar o que estão aprendendo.

---

## 🎯 Qual é o objetivo?

Este projeto fornece um ambiente Docker com uma instância do RabbitMQ pronta para uso. Junto com ele, temos scripts Python básicos de "Produtor" e "Consumidor" para que vocês possam:

* Entender visualmente o fluxo de uma mensagem.
* Ver como as filas (Queues) e Exchanges funcionam.
* Testar diferentes cenários (ex: o que acontece se o consumidor cair?).
* Praticar a criação de novas filas, rotas e tipos de exchanges.

## 🤔 O que é RabbitMQ? (A Versão Simples)

Pense no RabbitMQ como um **carteiro inteligente** para aplicações.

* **Producer (Produtor):** É quem escreve uma carta (mensagem) e entrega ao carteiro.
* **Exchange (Agência dos Correios):** É para onde o produtor envia a carta. A exchange decide para qual fila deve mandar, baseado em regras (o "endereço").
* **Queue (Fila / Caixa Postal):** Onde as cartas ficam armazenadas, esperando para serem lidas.
* **Consumer (Consumidor):** É quem vai até a caixa postal, pega a carta e a lê.

Nosso trabalho como desenvolvedores é configurar esse fluxo: dizer ao produtor para qual "agência" enviar, configurar as regras da "agência" e dizer ao consumidor de qual "caixa postal" ele deve ler.

---

## 🚀 Como Começar (O Guia Rápido)

Você só precisa ter o **Docker** e o **Docker Compose** instalados na sua máquina.

### Passo 1: Iniciar o RabbitMQ

1.  Clone este repositório:
    ```bash
    git clone [https://github.com/leonardoopa/rabbitmq_test.git](https://github.com/leonardoopa/rabbitmq_test.git)
    cd rabbitmq_test
    ```

2.  Suba o container do RabbitMQ:
    ```bash
    docker-compose up -d
    ```
    *Isso irá iniciar o RabbitMQ em background.*

### Passo 2: Ver o Painel de Controle

O RabbitMQ vem com um painel de gerenciamento visual muito útil.

1.  Acesse no seu navegador: [**http://localhost:15672**](http://localhost:15672)
2.  Use o login e senha padrão:
    * **Usuário:** `guest`
    * **Senha:** `guest`

Dê uma olhada nas abas "Exchanges" e "Queues". Por enquanto, estará tudo quase vazio.

### Passo 3: Preparar o Ambiente Python

Vamos usar os scripts `producer.py` e `consumer.py` para interagir com o Rabbit.

1.  Recomendo criar um ambiente virtual (venv):
    ```bash
    python -m venv venv
    source venv/bin/activate  # (No Windows: .\venv\Scripts\activate)
    ```

2.  Instale a biblioteca Pika (o cliente Python do RabbitMQ):
    ```bash
    pip install pika
    ```

### Passo 4: A Mágica!

Agora, vamos ver tudo funcionando.

1.  Abra **dois terminais** diferentes (ambos com o `venv` ativado).

2.  **No Terminal 1 (Consumidor):**
    Execute o consumidor. Ele vai ficar "escutando" por mensagens na fila.
    ```bash
    python consumer/consumer.py
    ```
    *(Você verá uma mensagem "Aguardando mensagens...")*

3.  **No Terminal 2 (Produtor):**
    Execute o produtor para enviar uma mensagem.
    ```bash
    python producer/producer.py
    ```

**O que deve acontecer?**
Assim que você rodar o `producer.py`, a mensagem "Olá, mundo!" (ou qualquer outra que esteja no script) aparecerá instantaneamente no **Terminal 1**!

**Parabéns!** Você acabou de enviar sua primeira mensagem com RabbitMQ.

---

## 💡 Ideias para "Brincar" (Testes)

Agora é com vocês. Usem a base que temos para testar cenários.

* **Teste 1: Mensagens Diferentes**
    * Abra o `producer/producer.py` e mude a mensagem (`body='Olá, mundo!'`).
    * Rode o produtor várias vezes. Veja as mensagens chegando no consumidor.

* **Teste 2: Durabilidade da Fila**
    * **Desligue** o consumidor (dê `Ctrl+C` no Terminal 1).
    * Rode o produtor (`producer.py`) várias vezes (ex: 5 vezes).
    * Agora, **ligue** o consumidor (`consumer/consumer.py`) novamente.
    * **Pergunta:** As mensagens que você enviou "enquanto ele estava offline" chegaram? Por quê? (Dica: olhe a declaração da fila no código).

* **Teste 3: Múltiplos Consumidores**
    * Abra *mais um* terminal (agora são 3).
    * No Terminal 3, rode o `consumer.py` também.
    * Agora você tem *dois* consumidores rodando.
    * Rode o `producer.py` 10 vezes.
    * **Pergunta:** Como as mensagens foram distribuídas entre os dois consumidores? (Isso é o *Round-Robin*).

* **Teste 4: Criando sua Própria Fila**
    * No `producer.py` e `consumer.py`, mude o nome da fila (`queue='hello'`) para algo novo, como `queue='fila_teste'`.
    * Rode o consumidor e depois o produtor.
    * Vá no painel de controle (http://localhost:15672) e veja sua nova fila criada na aba "Queues".

* **Desafio: Fanout (Broadcast)**
    * Crie dois consumidores (`consumer_A.py`, `consumer_B.py`) que leem de filas diferentes (`fila_A`, `fila_B`).
    * Crie um produtor que envia a mensagem para uma **Exchange do tipo `fanout`**.
    * Configure a exchange para que ela envie a *mesma* mensagem para *ambas* as filas (`fila_A` e `fila_B`).
    * Rode os dois consumidores, rode o produtor e veja a mensagem ser "transmitida" para os dois ao mesmo tempo.

---

## ❓ Dúvidas?

Não guarde perguntas! Me chame (ou qualquer outro membro do time) para conversarmos. O objetivo é aprender.

Divirtam-se!
