"""これがメインファイル
"""
import sys
import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import compass
import serialHandler as sh
import vincenty


MAGNETIC_DECLINATION = -7.93  # degree east:+, west:-


class Application(tk.Frame):
    def __init__(self, master=None):
        ### for debug ###
        self.heading_azimuth_dummy = 0
        #################
        # 数値初期化
        self.distance = 0.0
        self.target_azimuth = 0
        self.heading_azimuth = 0
        self.heading_latitude = 0.0     # 現在地緯度
        self.heading_longitude = 0.0    # 　　　経度
        self.target_latitude = 0.0      # 目標緯度
        self.target_longitude = 0.0     # 　　経度

        # 諸々初期化
        self.compass = compass.Compass()
        # self.serial = sh.SerialHandler()

        # Tkinter初期化
        super().__init__(master)
        self.master = master
        self.master.title('GPS finder')
        self.pack()
        self.create_widgets()
        self.master.after(500, self.update_widgets)

    def create_widgets(self):
        # グラフ
        self.frame_canvas = tk.Frame(self.master)
        self.frame_canvas.pack(side=tk.LEFT)
        #   コンパス
        self.canvas = FigureCanvasTkAgg(
            self.compass.fig, master=self.frame_canvas)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        # 情報
        self.frame_info = tk.Frame(self.master)
        self.frame_info.pack(side=tk.RIGHT)

        self.info_text_heading = tk.Label(
            self.frame_info, text='heading', fg='red')
        self.info_data_heading = tk.Label(self.frame_info, text=0)
        self.info_text_target = tk.Label(
            self.frame_info, text='target', fg='green')
        self.info_data_target = tk.Label(self.frame_info, text=0)
        self.info_text_distance = tk.Label(self.frame_info, text='distance')
        self.info_data_distance = tk.Label(self.frame_info, text=0)

        labels = [self.info_text_heading,
                  self.info_data_heading,
                  self.info_text_target,
                  self.info_data_target,
                  self.info_text_distance,
                  self.info_data_distance]
        [label.pack() for label in labels]

    def update_widgets(self):
        ### DUMMY INPUT ###
        if self.heading_azimuth_dummy == 364:
            self.heading_azimuth_dummy = 0
        self.heading_azimuth_dummy += 4
        self.heading_azimuth = self.heading_azimuth_dummy
        self.heading_latitude = 38.260295
        self.heading_longitude = 140.882385  # 仙台駅
        self.target_latitude = 38.255435
        self.target_longitude = 140.840823  # 創造工学センター
        ###################

        # ### TRUE INPUT ###
        # self.serial.update()
        # self.unpack_data(self.serial.data)
        # ##################

        # 目標方位・距離計算
        vincenty_dict = vincenty.vincenty_inverse(self.heading_latitude,
                                                  self.heading_longitude,
                                                  self.target_latitude,
                                                  self.target_longitude,
                                                  ellipsoid='WGS84')
        self.distance = vincenty_dict['distance']
        self.target_azimuth = vincenty_dict['azimuth12']

        # 地磁気偏角補正
        self.heading_azimuth = int(self.heading_azimuth + MAGNETIC_DECLINATION)
        if self.heading_azimuth < 0:
            self.heading_azimuth += 360
        self.target_azimuth = int(self.target_azimuth + MAGNETIC_DECLINATION)
        if self.target_azimuth < 0:
            self.target_azimuth += 360

        # 描画更新
        self.compass.update(self.heading_azimuth, self.target_azimuth)
        self.canvas.draw()

        self.update_info(self.heading_azimuth,
                         self.target_azimuth, self.distance)

        self.master.after(500, self.update_widgets)

    def update_info(self, heading_azimuth, target_azimuth, distance):
        self.info_data_heading['text'] = heading_azimuth
        self.info_data_target['text'] = target_azimuth
        self.info_data_distance['text'] = int(distance)

    def unpack_data(self, data):
        self.heading_azimuth = data[0]
        self.heading_latitude = data[1]
        self.heading_longitude = data[2]
        self.target_latitude = data[3]
        self.target_longitude = data[4]


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
