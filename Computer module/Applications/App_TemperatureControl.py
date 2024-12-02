from brokerClient import BrokerClient

service_id = 10
client = BrokerClient(service_id=service_id)
client.start()

# getAnalog Module 2
def getTemperature():
    level = 0

# setAnalog Module 1
def setFanSpeed():
    level = 0

#setDigital Module 1
def setTemperatureIndicator():
    level = 0


def map_temperatureToFanSpeed(Temperature):
    level = 0


while(1):

    Temperature = getTemperature()

    setFanSpeed(map_temperatureToFanSpeed(Temperature))


    if Temperature <= 30:
        setTemperatureIndicator("low")

    if 30 < Temperature <= 60:
        setTemperatureIndicator("medium")

    if Temperature > 60:
        setTemperatureIndicator("High")


#•	Enquanto a temperatura(Trimpot 2 M1) estiver entre 0 a 30% LED 4 M1: Indicando um nível de umidade baixo (ex: vermelho).
#•	Enquanto a temperatura(Trimpot 2 M1)  estiver entre 30% a 60% LED 5 M1: Indicando um nível de umidade baixo (ex: vermelho).
#•	Enquanto a temperatura(Trimpot 2 M1)  estiver entre 60% a 100% LED  6 m1: Indicando um nível de umidade baixo (ex: vermelho).
#•	LED PWM 1(ventilação) deve ta o mais for possivel quando a  temperatura for maxima, e o mais fraco possivel quando a temperatura estiver minima

