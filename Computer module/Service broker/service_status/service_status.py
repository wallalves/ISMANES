import json

class ServiceStatus:
    def __init__(self, catalogPath):
        self.catalogPath = catalogPath
        self.catalog = None  # Variável para armazenar o catálogo
        self.status = {}  # Será um dicionário {"id": "status"}
        self.loadCatalog()
        self.CreateStatusList()

    def loadCatalog(self):
        if self.catalog is None:  # Carrega o catálogo apenas se ainda não foi carregado
            with open(self.catalogPath, 'r') as file:
                self.catalog = json.load(file)
        return self.catalog

    def CreateStatusList(self):
        # Gera o dicionário com "id": "unavailable" para cada serviço
        self.status = {service["id"]: "unavailable" for service in self.catalog}

    def checkStatus(self, serviceID):
        # Retorna o status de um serviço pelo ID ou uma mensagem padrão se não encontrado
        return self.status.get(serviceID, "Serviço não encontrado")

#CatalogPath = "Computer module\Catalogs\ServiceCatalog.json"
#st = ServiceStatus(CatalogPath)
#print(st.status)