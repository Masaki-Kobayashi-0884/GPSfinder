import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np


class Compass():
    def __init__(self):
        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(111)

        # 羅針盤作成
        self.ax.axis('off')
        self.ax.axis('scaled')
        self.ax.set_aspect('equal')
        self.ax.set_xlim(-1.2, 1.2)
        self.ax.set_ylim(-1.2, 1.2)

        self.circle = self.ax.add_patch(patches.Circle(xy=(0, 0), radius=1, fill=False, ec='k'))
        self.ax.plot([-1, 1], [0, 0], c='k')
        self.ax.plot([0, 0], [-1, 1], c='k')
        self.ax.plot([-2**0.5/2, 2**0.5/2], [-2**0.5/2, 2**0.5/2], c='k')
        self.ax.plot([-2**0.5/2, 2**0.5/2], [2**0.5/2, -2**0.5/2], c='k')

        self._draw_arrows(0, 0)
    
    def update(self, heading_azimuth, target_azimuth):
        self.arrow_heading.remove()
        self.arrow_target.remove()
        self._draw_arrows(heading_azimuth, target_azimuth)

    def _azimuth2arrow_coordinate(self, azimuth):
        pol = (450 - azimuth) % 360
        x = np.cos(np.deg2rad(pol))
        y = np.sin(np.deg2rad(pol))
        arrow_coordinate = [-x, -y, 2*x, 2*y]
        return arrow_coordinate
    
    def _draw_arrows(self, heading_azimuth, target_azimuth):
        # 向いてる方向
        arrow_heading_coordinate = self._azimuth2arrow_coordinate(heading_azimuth)
        self.arrow_heading = self.ax.arrow(*arrow_heading_coordinate,
                                           width=0.02,
                                           head_width=0.05,
                                           head_length=0.1,
                                           length_includes_head=True,
                                           color='red')

        # 目標の方向
        arrow_target_coordinate = self._azimuth2arrow_coordinate(target_azimuth)
        self.arrow_target = self.ax.arrow(*arrow_target_coordinate,
                                          width=0.02,
                                          head_width=0.05,
                                          head_length=0.1,
                                          length_includes_head=True,
                                          color='green')
        
        
if __name__ == "__main__":
    c = Compass()
    plt.show()