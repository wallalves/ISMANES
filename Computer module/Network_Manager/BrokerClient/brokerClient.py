import socket
import threading
import json
import time

class BrokerClient:
    def __init__(self, client_id, broker_host='127.0.0.1', broker_port=5000, ):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.client_id = client_id
        self.socket = None
        self.running = True
        self.broker_receive_callback = None

    def set_broker_receive_callback(self, callback):
        self.broker_receive_callback = callback

    def connect_to_broker(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.broker_host, self.broker_port))
            print(f"Conectado ao broker em {self.broker_host}:{self.broker_port}")

            # Aguarda o broker solicitar o ID de serviço
            data = self.socket.recv(1024)
            if data:
                request = json.loads(data.decode())
                if request.get("type") == "request_client_id":
                    # Envia o ID de serviço
                    self.socket.sendall(json.dumps({"client_id": self.client_id}).encode())
                    print(f"ID de serviço enviado: {self.client_id}")
                else:
                    raise ValueError("Mensagem inesperada do broker.")
        except Exception as e:
            print(f"Erro ao conectar ao broker ou enviar o ID de serviço: {e}")
            self.running = False
            return False

        return True

    def read_messages(self):
        # Thread para ler mensagens da fila do broker
        while self.running:
            try:
                # Envia requisição para ler a próxima mensagem
                self.socket.sendall(json.dumps({"type": "read"}).encode())
                data = self.socket.recv(1024)
                if data:
                    json_package = json.loads(data.decode())

                    # Leitura bem sucedida
                    if json_package.get("status") == "success":
                        # Chama o Callback para enviar essa mensagem recebida para a serial
                        if self.broker_receive_callback:
                            self.broker_receive_callback(json_package)

                        print(f"\n ~~ Mensagem recebida de [{json_package['sender']}]: {json_package['message']}")

                    # Fila vazia
                    elif json_package.get("status") == "error" and json_package.get("message") == "Fila vazia":
                        time.sleep(1)  # Aguarda antes de consultar novamente

                    # erro na leitura
                    else:
                        print(f"Erro ao ler mensagem: {json_package}")

            except Exception as e:
                print(f"Erro ao ler mensagens do broker: {e}")
                break
        #Close socket when the thread ends
        self.socket.close()

    def send_message(self, recipient_ID, encoded_package ):
        try:
            recipient_id = recipient_ID
            package = encoded_package
            self.socket.sendall(json.dumps({
                "type": "send",
                "recipient": recipient_id,
                "message": package
            }).encode())

            response = self.socket.recv(1024)
            if response:
                response_data = json.loads(response.decode())
                if response_data.get("status") == "success":
                    return True
                else:
                    return False
                
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
            self.running = False
            return False

    def start(self):
        # Tenta se conectar ao broker
        try:
            if not self.connect_to_broker():
                print("Falha na conexão com o broker!")
                return
            # Inicia a thread para leitura de mensagens
            thread = threading.Thread(target=self.read_messages, daemon=True)
            thread.start()
        except:
            print("Conexão recusada.")
            return
            # Inicia o envio de mensagens
            #self.send_message()