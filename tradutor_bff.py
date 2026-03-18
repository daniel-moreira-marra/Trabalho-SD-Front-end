import asyncio
import websockets
import json

# Guarda todos os navegadores conectados para atualizar a tela de todos juntos
clientes_conectados = set()

async def handle_client(websocket):
    clientes_conectados.add(websocket)
    print(f"🟢 Nova aba conectada. Total de clientes na interface: {len(clientes_conectados)}")
    
    try:
        async for ws_message in websocket:
            front_data = json.loads(ws_message)
            
            # 1. Estrutura pura TCP que o nosso Rust original exige
            rust_request = {
                "source_id": front_data.get("user", "Desconhecido"),
                "payload": front_data.get("message", ""),
                "timestamp": 0,
                "is_concurrent": False
            }
            rust_json = json.dumps(rust_request) + "\n"
            
            try:
                # 2. Bate no Load Balancer (Nginx) na porta 8080 via TCP
                reader, writer = await asyncio.open_connection('127.0.0.1', 8080)
                writer.write(rust_json.encode('utf-8'))
                await writer.drain()
                
                # 3. Lê a resposta processada pelo Relógio de Lamport
                rust_response_bytes = await reader.readline()
                rust_response_str = rust_response_bytes.decode('utf-8').strip()
                
                if rust_response_str:
                    rust_data = json.loads(rust_response_str)
                    
                    # 4. Traduz de volta para a interface visual
                    front_response = {
                        "user": rust_data.get("source_id"),
                        "message": rust_data.get("payload"),
                        "timestamp": front_data.get("timestamp", "00:00"), 
                        "lamport": rust_data.get("timestamp"),    
                        "node": 1, # Representa o Gateway
                        "is_concurrent": rust_data.get("is_concurrent", False),
                        "forwarder_id": rust_data.get("forwarder_id")
                    }
                    
                    response_json = json.dumps(front_response)
                    
                    # 5. Mágica visual: envia a mensagem para TODAS as abas conectadas!
                    for cliente in clientes_conectados:
                        await cliente.send(response_json)
                    
                writer.close()
                await writer.wait_closed()
                
            except ConnectionRefusedError:
                print("🔴 Erro: O Docker está desligado! Ligue o docker-compose.")
                
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        clientes_conectados.remove(websocket)
        print(f"🔴 Aba fechada. Total de clientes na interface: {len(clientes_conectados)}")

async def main():
    async with websockets.serve(handle_client, "localhost", 8081):
        print("🚀 Super Tradutor BFF rodando em ws://localhost:8081")
        print("Aguardando as abas do navegador conectarem...")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())