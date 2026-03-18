# 💻 Front-end | Chat Distribuído (Relógios de Lamport)

Este repositório contém a interface visual e a camada de integração do nosso trabalho de Sistemas Distribuídos (Tema 2 - Chat com Relógios de Lamport). 

Ele foi projetado para operar em conjunto com o repositório do Back-end (`Trab-SD-Back-end`), unindo uma interface moderna e minimalista com a robustez e o rigor técnico da comunicação TCP do núcleo em Rust.

## 🌉 A Mágica da Integração: O Padrão BFF (Tradutor)

Navegadores web modernos bloqueiam conexões TCP puras por motivos de segurança da *sandbox*, exigindo o uso de protocolos como WebSocket. Como o requisito do nosso Back-end é operar estritamente via TCP, implementamos o padrão arquitetural **BFF (Backend for Frontend)**.

Junto aos arquivos de interface, utilizamos o script `tradutor_bff.py`. Ele atua como um *middleware* tradutor em tempo real:
1. Recebe as conexões via **WebSocket** originadas do navegador.
2. Formata a mensagem e a dispara via **TCP Puro** para o Load Balancer (Nginx) do Back-end.
3. Recebe a resposta processada (com os Relógios de Lamport atualizados pelo Rust), converte de volta para o formato web e a distribui simultaneamente para todas as abas abertas, refletindo o *broadcast* da rede distribuída.

## 🧠 A Inteligência da Interface

O Front-end atua de forma ativa para organizar e exibir os eventos da rede de forma coesa. O fluxo de inteligência funciona assim:

1. **Motor de Ordenação (Ordem Total):** Como a rede tem latência, as mensagens podem chegar fora de ordem cronológica. Sempre que um novo JSON é recebido, o JavaScript reordena o histórico do chat aplicando as regras matemáticas do algoritmo:
   - Ordenação primária pelo menor relógio lógico (`lamport`).
   - Em caso de simultaneidade (empate), o desempate para garantir a ordem total é feito pelo identificador de origem (`user`).
2. **Dashboard Dinâmico:** O painel lateral monitora e exibe dinamicamente estatísticas da rede, como o avanço temporal do maior Relógio de Lamport alcançado.
3. **Detecção de Concorrência:** Mensagens identificadas pelo núcleo Rust como desprovidas da relação "Aconteceu-Antes" ganham destaque visual imediato através de uma *badge* (`⚠️ Concorrente`).

## 🚀 Como subir o ambiente

Para testar o Front-end, é obrigatório que a infraestrutura do **Back-end já esteja em execução** (via `docker-compose up` na pasta referente ao núcleo Rust/Nginx).

**Passo a passo na pasta deste repositório (Front-end):**

1. Instale a dependência necessária para o tradutor Python, caso ainda não possua:
   ```bash
   pip3 install websockets

2. Inicie o serviço de tradução do Python BFF (Back For Front):
   ```bash
   python3 tradutor_bff.py

3. Localize e dê um duplo clique no arquivo HTML da página do Front-end na árvore de arquivos do computador.