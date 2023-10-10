import time
import board
import busio
import digitalio
import adafruit_rfm9x
from analogio import AnalogIn
from digitalio import DigitalInOut
uart = busio.UART(board.TX, board.RX, baudrate=9600)

RADIO_FREQ_MHZ = 915.0
CS = digitalio.DigitalInOut(board.RFM9X_CS)
RESET = digitalio.DigitalInOut(board.RFM9X_RST)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)
rfm9x.tx_power = 20
rfm9x.enable_crc = True
rfm9x.ack_retries = 10
rfm9x.ack_delay = 0.2
rfm9x.ack_wait = 1
rfm9x.xmit_timeout = 0.2
rfm9x.signal_bandwidth = 500000
rfm9x.spreading_factor = 10
rfm9x.node = 24
rfm9x.destination = 7
def send(data, destination, with_ack=False) -> bool:
    rfm9x.destination = int(destination)
    rfm9x.send(bytes(data, 'UTF-8'))
    if with_ack:
        return rec_ack()
def send_ack(destination):
    rfm9x.destination = destination
    rfm9x.send(b"ok")
def rec_ack():
    packet = rfm9x.receive(
        with_ack=False, with_header=True, timeout=0.1, keep_listening=True
    )
    if packet is not None:
        if packet[4:] == b"ok":
            return True
        else:
            return False
    else:
        return False
def FTotal(response):
    Total = str(response[-11:-7])
    data = ('Flujo' + '/' + Total)
    return data

while True:
    packet = rfm9x.receive(with_ack=False, with_header=True, timeout=100.0, keep_listening=True)
    try:
        paquete = str(packet[4:], "ascii")
    except:
        continue

    if paquete == "Data!{0}".format(rfm9x.node):
        print("Midiendo...")
        uart.write(bytes("1", "utf-8"))
        response = str(uart.read())
        data = FTotal(response)
        #print(data)

        print("Datos a enviar: {}".format(data))
        #send_ack(int(packet[1]))
        try:
            rfm9x.send(bytes(data, "UTF-8"))
        except:
            continue
        ack = rec_ack()
        while not ack:
            print("Acknowledge {}".format(ack))
            rfm9x.send(bytes(data, "UTF-8"))
            ack = rec_ack()
            break
