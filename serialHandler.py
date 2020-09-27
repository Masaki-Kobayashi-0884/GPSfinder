import re
import time

import serial
from serial.tools import list_ports


class SerialHandler():
    """シリアル通信ハンドラ

    シリアル通信から数値のリストへ変換するまでを行う
    COMポートは指定したほうが無難

    Args:
        port(str, optional): ポートを選択 初期値 自動選択
        baudrate(int, optional): ボーレートを設定 初期値 115200
        timeout(int, optional): タイムアウトを設定 初期値 1

    Attitudes:
        data(list[float]): 整形されたデータが収納される。更新は update() で
        re_pattern(str): データ抽出用の正規表現パターン /nと/rに挟まれた部分を抽出している
        ser(serial.Serial): pyserial
    """

    def __init__(self, port=None, baudrate=115200, timeout=1):
        self.data = []
        self.re_pattern = r'\n.+\r'

        if port is None:
            ports = list_ports.comports()
            if ports == []:
                print("cannot find comport")
            port = ports[0].device
        
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(3)
        print("serial init end")

    def __del__(self):
        self.ser.close()

    def update(self):
        """インスタンス変数 data を更新

        returns:
            bool: True なら成功 False なら失敗 data の変化なし
        """
        # 元データ -> デコード -> /nと/rに囲まれている部分を検索 -> 最新のものを数値のリストに
        data_raw = self.ser.read_all().decode()
        data_list = re.findall(self.re_pattern, data_raw)

        if data_list == []:
            return False

        data_str = data_list[-1].strip().split(',')
        self.data = [float(s) for s in data_str]

        return True


if __name__ == "__main__":
    ser = SerialHandler()
    while True:
        ser.update()
        print(ser.data)
        time.sleep(1)
