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
        self.readCallback = None

    def set_read_callback(self, callback):
        """
        Define a função de callback que será chamada quando uma mensagem for recebida.

        :param callback: Função que será chamada ao receber uma mensagem (deve aceitar um parâmetro: bytes).
        """
        self.readCallback = callback

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
                    response = json.loads(data.decode())

                    # Leitura bem sucedida
                    if response.get("status") == "success":
                        # Chama o Callback para enviar essa mensagem recebida para a serial
                        if self.readCallback:
                            self.readCallback(response)
                        print(f"\n ~~ Mensagem recebida de [{response['sender']}]: {response['message']}")

                    # Fila vazia
                    elif response.get("status") == "error" and response.get("message") == "Fila vazia":
                        time.sleep(1)  # Aguarda antes de consultar novamente

                    # erro na leitura
                    else:
                        print(f"Erro ao ler mensagem: {response}")

            except Exception as e:
                print(f"Erro ao ler mensagens do broker: {e}")
                break
        #Close socket when the thread ends
        self.socket.close()

    def send_message(self, recipient_ID, Message ):
        try:
            recipient_id = recipient_ID
            message = Message.hex()
            self.socket.sendall(json.dumps({
                "type": "send",
                "recipient": recipient_id,
                "message": message
            }).encode())
            response = self.socket.recv(1024)
            if response:
                response_data = json.loads(response.decode())
                if response_data.get("status") == "success":
                    print("Mensagem enviada com sucesso.")
                else:
                    print(f"Erro ao enviar mensagem: {response_data['message']}")
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
            self.running = False
            return

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

#if __name__ == "__main__":
#    # Solicita o ID de serviço no início
#    client_id = input("Digite seu ID de serviço: ").strip()
#    client = Client(client_id=client_id)
#    client.start()

    #while(1):