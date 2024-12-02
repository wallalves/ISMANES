from serialNetwork import SerialNetwork

if __name__ == "__main__":
    def my_callback(message):
        """Função de callback chamada quando uma mensagem é recebida."""
        print(f"Callback ativado! Mensagem recebida: {message}")

    serial = SerialNetwork(port="COM10", baudrate=115200)

    try:
        serial.set_message_callback(my_callback)  # Define o callback
        serial.connect()


        serial.send(b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C')  # Exemplo de envio binário
        serial.send(b'\x01\x01\x01\x01\x02\x02\x02\x02\x03\x03\x03\x03')  # Exemplo de envio binário
        serial.send(b'\x00\x05\x00\x05\x00\x10\x10\x00\x20\x40\x60\x80')  # Exemplo de envio binário

        while(True):
            False

    finally:
        serial.disconnect()