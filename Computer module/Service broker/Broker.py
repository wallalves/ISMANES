import socket
import threading
import json
from collections import deque
from Logger.Logger import Logger
from service_status.service_status import ServiceStatus

# Caminho para o catálogo de serviços
serviceCatalog = "Computer module\\Catalogs\\ServiceCatalog.json"

class Broker:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(200)
        self.service_status = ServiceStatus(serviceCatalog)
        self.log = Logger("Broker_")
        self.log.log(f'Broker ouvindo na porta {self.port}',self.log.logtype_info)
        
        # Dicionário para armazenar as filas de mensagens por ID de serviço
        self.client_queues = {}

    def handle_client(self, client_socket, client_address):        
        client_name = [service["name"] for service in self.service_status.catalog if service["id"] == client_address]        
        self.log.log(f'Nova conexão Requisitada por {client_address}',self.log.logtype_info)
        
        # Solicita o client_id ao cliente
        client_id = self.get_client_id_from_client(client_socket)
        
        # Se o ID for retornado com sucesso e estiver presente no catalogo 
        # Inicia os preparativos -- > Criação da fila de mensagem associada ao ID
        # O ID 0 não será utilizado no catalogo
        if client_id and self.is_client_id_in_catalog(client_id):

            self.client_queues[client_id] = deque()
            client_name = [ service["name"] for service in self.service_status.catalog if service["id"] == client_id]
            client_type = [ service["type"] for service in self.service_status.catalog if service["id"] == client_id]

            self.client_queues[client_id].append({
                "message": "Acepted",
                "sender": "broker"  # Adiciona o ID do remetente
            })
            
            self.log.log(f'Conexão aceita para o cliente {client_name} [ type = {client_type} ] [ ID = {client_id} ]',self.log.logtype_info)

        #Se o id ao for encontrado ou for invalido, encerra o socket e a thread.
        else:            
            self.log.log(f'ID de cliente {client_id} não encontrado no catálogo. Encerrando conexão.',self.log.logtype_error)
            client_socket.sendall(json.dumps({
                "status": "error",
                "message": "ID de serviço inválido ou não encontrado no catálogo."
            }).encode())
            client_socket.close()
            return

        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break

                message = json.loads(data.decode())  # Parse a mensagem JSON
                print(f'dados recebidos : {message}')
                if message['type'] == 'read':
                    # O cliente quer ler a próxima mensagem
                    response = self.read_message(client_id)
                    client_socket.sendall(json.dumps(response).encode())

                elif message['type'] == 'send':
                    # O cliente quer enviar uma mensagem para outro cliente
                    recipient_id = message.get('recipient')
                    if recipient_id in self.client_queues:
                        # Coloca a mensagem na fila do destinatário, incluindo o remetente
                        self.client_queues[recipient_id].append({
                            "message": message['message'],
                            "sender": client_id  # Adiciona o ID do remetente
                        })
                        self.log.log(f'Mensagem enfileirada para {recipient_id}',self.log.logtype_info)

                        client_socket.sendall(json.dumps({
                            "status": "success",
                            "message": "Mensagem enviada",
                            "sender": "broker",
                            "recipient": client_id
                        }).encode())
                    else:
                        # Destinatário não encontrado
                        client_socket.sendall(json.dumps({
                            "status": "error",
                            "message": "Destinatário não encontrado",
                            "sender": "broker",
                            "recipient": client_id
                        }).encode())
            except ConnectionResetError:
                break
        
        # Remove a fila do serviço ao desconectar
        if client_id in self.client_queues:
            del self.client_queues[client_id]
        
        client_socket.close()
        self.log.log(f'Conexão encerrada: {client_address}',self.log.logtype_error)
        

    def start(self):
        while True:
            client_socket, client_address = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            thread.start()

    def read_message(self, client_id):
        # Função para ler a próxima mensagem da fila do serviço
        if client_id in self.client_queues:
            queue = self.client_queues[client_id]
            if queue:
                message_data = queue.popleft()  # Retorna a primeira mensagem na fila
                return {
                    "status": "success",
                    "message": message_data["message"],  # Conteúdo da mensagem
                    "sender": message_data["sender"],  # Remetente
                    "recipient": client_id
                }
            else:
                return {
                    "status": "error",
                    "message": "Fila vazia",
                    "sender": "broker",
                    "recipient": client_id
                }
        return {
            "status": "error",
            "message": "Fila não encontrada",
            "sender": "broker",
            "recipient": client_id
        }

    def get_client_id_from_client(self, client_socket):
        # Esta função busca o ID de serviço do cliente
        try:
            client_socket.sendall(json.dumps({
                "type": "request_client_id",
                "message": "Informe seu ID de serviço (client_id)"
            }).encode())
            data = client_socket.recv(1024)
            if data:
                response = json.loads(data.decode())
                return response.get('client_id', None)
        except Exception as e:
            self.log.log(f'Erro ao obter client_id: {e}',self.log.logtype_error)
            return None

    def is_client_id_in_catalog(self, client_id):
        # Verifica se o client_id está no catálogo
        return any(service["id"] == client_id for service in self.service_status.catalog)

if __name__ == "__main__":
    broker = Broker()
    broker.start()
