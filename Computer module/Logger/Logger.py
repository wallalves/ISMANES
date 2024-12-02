import datetime
import os

class Logger:
    def __init__(self, base_log_file_name="appLog"):
        self.logtype_info = "INFO   "
        self.logtype_warning ="WARNING"
        self.logtype_error ="ERROR  "
        # Cria o diretório de logs, se não existir
        log_dir = os.path.join(os.path.dirname(__file__), "log")
        os.makedirs(log_dir, exist_ok=True)

        # Adiciona data e hora ao nome do arquivo de log
        timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        log_file_name = f"{base_log_file_name}_{timestamp}.txt"

        # Caminho completo para o arquivo de log
        self.log_file = os.path.join(log_dir, log_file_name)

        # Registra a inicialização do logger
        try:
            with open(self.log_file, 'a', encoding='utf-8') as file:
                file.write(f"Logger iniciado em {self._get_timestamp()}\n")
        except Exception as e:
            print(f"Erro ao inicializar o Logger: {e}")

    def log(self, message, level="INFO"):

        # Formata o log com o nível
        log_entry = f"{self._get_timestamp()} [{level}] {message}"

        # Registra no arquivo
        try:
            with open(self.log_file, 'a', encoding='utf-8') as file:
                file.write(log_entry + '\n')
        except Exception as e:
            print(f"Erro ao gravar no arquivo de log: {e}")

        # Exibe no terminal
        print(log_entry)

    def _get_timestamp(self):

        return datetime.datetime.now().isoformat()



if __name__ == "__main__":
    logger = Logger()
    logger.log("Este é um log de exemplo.",logger.logtype_info)
    logger.log("Este é um aviso.", logger.logtype_warning)
    logger.log("Este é um erro crítico!", logger.logtype_error)
