from brokerClient import BrokerClient

service_id = 10
client = BrokerClient(service_id=service_id)
client.start()

# GetAnalog MODULE 1
def getUmidityValue():
    level = 0

# GetAnalog MODULE 2
def getWaterLevel():
    level = 0

# SetDigital MODULE 2
def activate_irrigation():
    level = 0

# setDigital MODULE 1
def  setUmidityIndicator(UmidityIndicator):
    level = 0

while(1):

    Umidity = getUmidityValue()
    WaterLevel = getWaterLevel()

    if (Umidity < 30) and (WaterLevel > 10):
        while Umidity < 80:
            activate_irrigation()

    if Umidity <= 30:
        setUmidityIndicator("low")

    if 30 < Umidity <= 60:
        setUmidityIndicator("medium")

    if Umidity > 60:
        setUmidityIndicator("High")


#   Condição: Quando o sensor de umidade (Trimpot 1 do Módulo 1) estiver abaixo de 30% E o nível de água no reservatório (Trimpot 1 do Módulo 2) for maior que 10%.
#   Ação: Ligue a irrigação (LED 1 do Módulo 2) até que o sensor de umidade chegue a 80%.
#	Enquanto a temperatura(Trimpot 2 M1) estiver entre 0 a 30% LED 1 M1: Indicando um nível de umidade baixo (ex: vermelho).
#	Enquanto a temperatura(Trimpot 2 M1)  estiver entre 30% a 60% LED 2 M1: Indicando um nível de umidade baixo (ex: vermelho).
#	Enquanto a temperatura(Trimpot 2 M1)  estiver entre 60% a 100% LED 2 M1: Indicando um nível de umidade baixo (ex: vermelho).
