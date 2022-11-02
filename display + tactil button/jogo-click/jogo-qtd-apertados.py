from machine import Pin
from machine import I2C
from pico_i2c_lcd import I2cLcd
import utime

RECORD_QTD = 0

def realizar_qtd_botao_pressionado(tempo: int, button: dict, lcd:dict, led_onboard: dict) -> int:
    """
    Realiza a contagem de clicks no botão realizado pelo jogador.

    Parameters
    ----------
    tempo : int
        Tempo que será permitido o click. Após o tempo terminar, o jogo acaba.
    button : dict
        Objeto contendo as informações do botão no raspberry pi pico.
    lcd : dict
        Objeto contendo as informações do led LCD no raspberry pi pico.
    led_onboard : dict
        Objeto contendo as informações do led onboard da placa.

    Returns
    -------
    int
        Quantidade de vezez que foi pressinado o botão.
    """
    lcd.putstr(f"Qtd pressionado:")
    timeout = utime.time() + tempo
    print(f"Time out... {tempo} segundos")

    count = 0
    while True:
        if button.value():
            count += 1
            led_onboard.toggle()
            lcd.move_to(5, 1)
            lcd.putstr(str(count))
            utime.sleep(0.2)
        if utime.time() > timeout:
            lcd.clear()
            lcd.putstr(f"FIM DE JOGO!")
            lcd.move_to(0, 1)
            lcd.putstr(f"Pontuacao: {count}")
            break
    
    return count


def realizar_scroll(text: str) -> str:
    """
    Método que realizar o scroll de uma string, para ser exebidida no modulo LCD 16x02.

    Parameters
    ----------
    text : str
        Texto que terá sua sequencia ajustada como uma fila.

    Returns
    -------
    str
        String com o texto voltando um caractere.
    """
    list_text = list(text)
    for idx, x in enumerate(list_text):
        aux = list_text[idx]

        if idx == len(list_text) - 1:
            break
        list_text[idx] = list_text[idx + 1]
        list_text[idx + 1] = aux
    saida = ''.join(list_text)

    return saida


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


def obter_led_onboard() -> dict:
    """
    Método responsável por obter o led onboard da placa.
    Para o mesmo, sempre será utilizado o pino 25.

    Returns
    -------
    dict
        Objeto contendo as informações do led onboard da placa.
    """
    led_onboard = Pin(25, Pin.OUT)
    return led_onboard


def obter_botao_obj(posicao_pino: int) -> dict:
    """
    Método responsável por objeter o botão externo (Táctil Push-Button).

    Parameters
    ----------
    posicao_pino : int
        Posição do botão na placa.

    Returns
    -------
    dict
        Objeto contendo as informações do botão no raspberry pi pico.
    """
    button = Pin(posicao_pino,Pin.IN, Pin.PULL_DOWN)

    return button


def iniciar_jogo() -> None:
    """
    Método para iniciar o "jogo". O mesmo funciona da seguinte forma:
        1. O jogador terá que clicar o mais rápido que puder durante 10 segundos (ou mais, caso ajustado).
        2. Após a rodada do jogador, será exibido a pontuação do mesmo.
        3. Logo após a pontuação, será exibido uma tela com um ranking do maior ponto e uma mensagem de "Deseja tentar novamente?".
        4. Caso o jogador queira jogar novamente, para subir de ranking, basta apenas clicar no botão e o jogo começará novamente.

        O mesmo depende de:
        * 1x - Raspberry Pi Pico
        * 1x - Táctil Push-Button
        * 1x - Display LCD 16x02
        * 6x - Jumper Macho/Macho
    """
    global RECORD_QTD
    lcd = obter_objeto_lcd()
    led_onboard = obter_led_onboard()
    led_onboard.value(1)
    button = obter_botao_obj(15)

    qtd = realizar_qtd_botao_pressionado(10, button, lcd, led_onboard)
    print(f"Pontuacao: {qtd}")

    if qtd >= RECORD_QTD:
        RECORD_QTD = qtd

    utime.sleep(5)
    lcd.clear()
    lcd.putstr(f"RECORD: {RECORD_QTD}")
    print(f"Recorde qtd: {RECORD_QTD}")
    text = "Deseja tentar novamente? "
    lcd.move_to(0, 1)
    lcd.putstr(text[0:15])
    utime.sleep(0.4)

    while True:
        text = realizar_scroll(text)
        lcd.move_to(0, 1)
        lcd.putstr(text[0:15])
        utime.sleep(0.4)
        if button.value():
            iniciar_jogo()


iniciar_jogo()
