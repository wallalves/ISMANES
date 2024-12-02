from brokerClient import BrokerClient

service_id = 10
client = BrokerClient(service_id=service_id)
client.start()

# getAnalog Module 2
def getWaterLevel():
    level = 0

# setDigital Module 2
def activateWaterPump():
    level = 0

# setDigital Module 2
def setTankIndicator():
    level = 0

while(1):

    WaterLevel = getWaterLevel()

    if (WaterLevel < 10):

        while WaterLevel < 100:
            activateWaterPump()

    if WaterLevel < 20:
        setTankIndicator("Critical")

    if WaterLevel == 100:
        setTankIndicator("Full")

#Condição: Quando o nível de água no reservatório (Trimpot 1 do Módulo 2) estiver abaixo de 10%.
#Ação:
#Ligue a bomba de água que abastece o reservatório até chegar em 80% (LED 2 do Módulo 2).


#Acenda o LED 3 (reservatório em estado crítico) até que o nível de água suba acima de 20%.
#Quando o nivel de agua do reservatorio for = 100%, ligue o LED 4 m2 I
