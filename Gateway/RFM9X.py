# librerias que se usan para interactuar con pines.
import board
# se usa para trabajar con protocolos de comunicacion seriales
import busio
# se usa para interactuar con los pines de la raspberrypi
import digitalio
# biblioteca de adafruit para usar el radio
import adafruit_rfm9x
# threads nativos de python
import threading
# queues nativas de python
import queue
# bibliotecas de tiempo
from datetime import datetime
import time
# biblioteca de matematicas
import math
# permite obtener paths del file system (direcciones)
import os.path
# regular expressions
import re


class RFM9X(object):
    def __init__(self, freq=915.0, power=23, node=42):
        # Define pins connected to the chip. Example for Raspberry Pi
        CS = digitalio.DigitalInOut(board.CE1)
        RESET = digitalio.DigitalInOut(board.D25)
        # Initialize SPI bus.
        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        # Initialize RFM radio
        self.rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, freq)
        # Enable CRC checking
        self.rfm9x.enable_crc = True
        # Reintentos de env�o del paquete antes de reportar un fallo
        self.rfm9x.ack_retries = 40
        # Delay entre el env�o de cada ACK
        self.rfm9x.ack_delay = 1
        # Tiempo que espera el hardware para transmitir el paquete
        self.rfm9x.xmit_timeout = 0.2
        # Tiempo de espera de la funci�n receive() cuando espera por un ack
        self.rfm9x.ack_wait = 0.2
        # Direcci�n del nodo central (Gateway)
        # 1 byte (0 a 255)
        self.rfm9x.node = node
        self.rfm9x.tx_power = power

    def send(self, data, destination, with_ack=False) -> bool:
        self.rfm9x.destination = int(destination)
        self.rfm9x.send(bytes(data, 'utf-8'))
        if with_ack:
            return self.rec_ack()

    def rec_ack(self) -> bool:
        packet = self.rfm9x.receive(with_ack=False, with_header=True, timeout=2, keep_listening=True)
        if packet is not None:
            if packet[4:].decode("UTF-8") == "ok":
                return True
            else:
                return False
        else:
            return False

    def send_ack(self, destination):
        self.rfm9x.destination = destination
        self.send("ok", destination)

    def receive(self, with_ack=False):
        packet = self.rfm9x.receive(with_ack=False, with_header=True, timeout=2, keep_listening=True)
        if packet is not None:
            node = (str(packet[1]))
            print("Received (raw header):", [hex(x) for x in packet[0:4]])
            print("Received (raw payload): {0}".format(packet[4:]))
            print("RSSI: {0}".format(self.rfm9x.last_rssi))
            if with_ack:
                self.send_ack(node)
            return packet[4:].decode("UTF-8")
        else:
            return
