import threading
import serial
import base64
from Logger.Logger import Logger

class SerialNetwork:
    def __init__(self, port, baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = None
        self.running = False
        self.receive_thread = None
        self.serial_receive_callback = None  # Função de callback para mensagens recebidas
        self.log = Logger('NetworManager_')

    def set_serial_receive_callback(self, callback):
        self.serial_receive_callback = callback

    def connect(self):
        try:
            self.serial_connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            self.running = True
            self.receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
            self.receive_thread.start()
            self.log.log(f'Conectado à porta {self.port} a {self.baudrate} bps.',self.log.logtype_info)

        except serial.SerialException as e:
            self.log.log(f'Erro ao conectar à porta {self.port}: {e}',self.log.logtype_error)

    def _receive_loop(self):
        while self.running:
            try:
                if self.serial_connection and self.serial_connection.in_waiting >= 12:
                    
                    # Lê exatamente 12 bytes da porta COM
                    package = self.serial_connection.read(12)
                    # Codifica o pacote recebido para suportar o envio via JSON
                    encoded_package = base64.b64encode(package).decode('utf-8')
                    self.log.log(f'Mensagem recebida: {package}',self.log.logtype_info)

                    # Chama o callback para tratar a mensagem, se definido
                    if self.serial_receive_callback:
                        self.serial_receive_callback(encoded_package)

            except serial.SerialException as e:
                self.log.log(f'Erro na leitura da porta {self.port}: {e}',self.log.logtype_error)
                self.running = False

    def send(self, package):        
        # decode package received in base64 format
        decoded_package = base64.b64decode(package)

        if self.serial_connection and self.serial_connection.is_open:
            try:
                if isinstance(decoded_package, bytes):
                    self.serial_connection.write(decoded_package)
                    self.log.log(f'Mensagem enviada (bruta): {decoded_package}',self.log.logtype_info)
                else:
                    print("Mensagem deve ser do tipo 'bytes'.")
                    self.log.log(f"Mensagem deve ser do tipo 'bytes'.",self.log.logtype_warning)
            except serial.SerialException as e:
                print(f"Erro ao enviar mensagem: {e}")
                self.log.log(f"Erro ao enviar mensagem: {e}",self.log.logtype_error)
        else:
            self.log.log(f"Conexão serial não está aberta.",self.log.logtype_warning)

    def disconnect(self):
        self.running = False

        if self.receive_thread and self.receive_thread.is_alive():
            self.receive_thread.join()

        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            self.log.log(f"Desconectado da porta {self.port}.",self.log.logtype_warning)



