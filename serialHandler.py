import time

import serial


class SerialHandler():
    DEFAULT_COM_PORT = 'COM3'
    DEFAULT_BAUD_RATE = 19200

    def __init__(self, port=DEFAULT_COM_PORT, rate=DEFAULT_BAUD_RATE):
        self.ser = serial.Serial(port, rate, timeout=1)
        print('initialize start')
        time.sleep(3)
        print('initialize end')
        self.list_float = []
    
    def __del__(self):
        self.ser.close()

    def update(self):
        self.ser.flushInput()
        raw = self.ser.readline()
        list_str = raw.strip().decode('utf-8').split(',')
        # print(list_str)
        try:
            self.list_float = [float(s) for s in list_str]
        except ValueError as e:
            print("Cought ValueError:", e)
        # return self.list_float


if __name__ == "__main__":
    s = SerialHandler()
    while True:
        s.update()
        print(s.list_float)
        time.sleep(1)
