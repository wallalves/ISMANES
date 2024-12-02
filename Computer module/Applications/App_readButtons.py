from BrokerClient.brokerClient import BrokerClient
import time

def readButton(response):

    if response['message'] == "Acepted":
        print(f'Conexão aceita!');
    else:
        print(f' mensagem recebida de {response['sender']}: {response['message']}')   
    return

client_id = 25
client = BrokerClient(client_id=client_id)
client.set_read_callback(readButton)
client.start()

while(True):
    data = b'\x00\x01\x00\x10\x02\xFF\x00\x00\x00\x00\x00\x00'
    client.send_message(1, data)
    time.sleep(5)