# 💻 Front-end | Chat Distribuído (Relógios de Lamport)

Este repositório contém a **Parte 3** do nosso trabalho de Sistemas Distribuídos. 

O objetivo aqui não é apenas exibir uma tela, mas sim resolver o problema da **ordenação assíncrona** das mensagens concorrentes usando os Relógios de Lamport no lado do cliente. A interface foi construída com um visual moderno, limpo e minimalista, garantindo que o foco principal fique na visualização em tempo real do funcionamento matemático dos nós.

## 🧠 A Inteligência do Front-end

O navegador atua de forma ativa para organizar os eventos da rede distribuída. O fluxo funciona assim:

1. **Tempo Real:** O front se comunica com os servidores via **WebSocket**, aguardando os pacotes de mensagens.
2. **Motor de Ordenação:** Como a rede tem latência, as mensagens podem chegar fora de ordem. Sempre que um novo JSON chega, o nosso JavaScript reordena o chat inteiro aplicando as regras do algoritmo:
   - Ordena pelo menor relógio lógico (`lamport`).
   - Em caso de simultaneidade (empate), o desempate é feito pelo menor ID de origem (`node`).
3. **Dashboard:** O painel lateral calcula e exibe dinamicamente estatísticas da rede, como o maior relógio de Lamport alcançado e o volume de mensagens.

## 🚀 Como subir o ambiente

Para cumprir os requisitos de infraestrutura, o frontend é servido de forma isolada por um **Nginx** rodando em um container Docker.

**Para rodar na sua máquina:**
1. Clone este repositório.
2. Abra o terminal na pasta do projeto e construa a imagem:
   ```bash
   docker build -t frontend-chat-lamport .