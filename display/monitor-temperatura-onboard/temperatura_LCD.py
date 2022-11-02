import utime
from machine import Pin, ADC
from machine import I2C
from pico_i2c_lcd import I2cLcd


def obter_objeto_lcd() -> dict:
    """
    Método responsável por configurar o modulo LCD externo, para ser utilizado via código.

    Returns
    -------
    dict
        Objeto contendo as informações do led LCD no raspberry pi pico.
    """
    Address = 0x27
    Rows = 2
    Cols = 16
    i2cConfig=I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
    lcd = I2cLcd(i2cConfig,Address,Rows, Cols)
    lcd.clear()

    return lcd 


def obter_temperatura_atual_sensor(temp_sensor: dict, fator_conversao: float) -> float:
    """
    Obtem a temperatura do sensor interno da placa e retorna o valor já convertido.

    Parameters
    ----------
    temp_sensor : dict
        Objeto contendo o sensor de temp onboard.
    fator_conversao : float
        Calculo para obter a temperatura em grau celsius.

    Returns
    -------
    float
        retorna a temperatura atual do sensor onboard da placa.
    """
    leitura = temp_sensor.read_u16() * fator_conversao 
    temperatura = 27 - (leitura - 0.706)/0.001721
    temp_atual = round(temperatura, 2)

    return temp_atual


temp_sensor = ADC(4)
fator_conversao = 3.3 / (65535)
temp_anterior = 0

lcd = obter_objeto_lcd()
 
while True:
    temp_atual = obter_temperatura_atual_sensor(temp_sensor, fator_conversao)

    if temp_atual != temp_anterior:
        lcd.clear()
        print("Temperatura: {}".format(temp_atual))
        lcd.putstr("TEMP: {} \xDFC".format(temp_atual))
        temp_anterior = temp_atual
    else:
        print(f"A temperatura continua a mesma. {temp_atual}")

    utime.sleep(2)
