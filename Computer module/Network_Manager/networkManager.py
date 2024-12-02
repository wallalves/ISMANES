import threading
from SerialNetwork.serialNetwork import SerialNetwork
from BrokerClient.brokerClient import BrokerClient

#armazena os clients de cada VMH para o envio das mensagens
VirtualModules = []

def receiveFromSerial(encoded_package):  
    packageType = encoded_package[4]
    recipient_ID = encoded_package[2]
    host_id = encoded_package[1]    

    # New Connection Request
    if packageType == "A":
        # Init virtual Module Handler threadConnection Request
        thread = threading.Thread(target=virtualModuleHandler, args=(host_id,))
        thread.start() 

    # Send Package Request
    if packageType == 0x20:
        #Data message
        VMclient = next((module["client"] for module in VirtualModules if module["id"] == host_id), None)
        if VMclient.send_message(recipient_ID, encoded_package) :
            VMclient.log.log(f"Mensagem enviada com sucesso.",VMclient.log.logtype_info)
        else:
            VMclient.log.log(f"Erro ao enviar mensagem.",VMclient.log.logtype_error)

def receiveFromBroker(json_package):
    data = json_package['message'] #base64
    serial.send(data)

def virtualModuleHandler(client_id):
    global VirtualModules
    #create a broker client instance
    client = BrokerClient(client_id=client_id)
    #save instance on virtual modules dict list to allow send messages to broker from this socket, out of this thread
    VirtualModules.append({"id": client_id, "client": client})
    #Set callback function to send messages received from broker to Serial
    client.set_broker_receive_callback(receiveFromBroker)
    #start client
    client.start()

# main loop
try:
    serial = SerialNetwork(port="COM10", baudrate=115200)
    serial.set_serial_receive_callback(receiveFromSerial)  # Define o callback
    serial.connect()
    while(True):
        False

finally:
    serial.disconnect()