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
        self.ser.write(str.encode('s'))
        raw = self.ser.readline()
        # print(raw)
        list_str = raw.strip().decode('utf-8').split(',')
        # print(list_str)
        try:
            self.list_float = [float(s) for s in list_str]
        except ValueError as e:
            print("Cought ValueError:", e)


if __name__ == "__main__":
    s = SerialHandler(rate = 115200)
    while True:
        s.update()
        print(s.list_float)
        time.sleep(1)
