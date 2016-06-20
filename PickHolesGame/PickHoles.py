#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '自动找茬游戏'
__author__ = 'pi'
__mtime__ = '6/18/2015-018'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
from PyQt5 import Qt
import win32gui
from PyQt5.QtGui import QColor, QPen, QPainter, QBitmap, QBrush, QPixmap
from PyQt5.QtWidgets import QWidget, QApplication
from numpy import zeros
import sys
import win32con
from PIL import ImageGrab
from Utility.Colors import DEFAULT, RED


class PickHoles(QWidget):
    IpClassName = "MozillaWindowClass"
    IpName = "游戏全屏 - Mozilla Firefox"
    ANCHOR_LEFT_X = 19  # 大图(包含左右两小图)左边界在窗口中的位置
    ANCHOR_Y = 174  # 大图上边界在窗口中的位置
    WIDTH = 780  # 大图宽
    HEIGHT = 520  # 大图高
    CLIP_WIDTH = 10  # 图形中比较剪切的大小
    CLIP_HEIGHT = 10
    DIFF_LIMIT = 2000  # 差异阀值，两片图形对比差异差异超过此值视为不一样
    result = None
    pixmap = None
    # size = WIDTH, HEIGHT

    def __init__(self, parent=None):
        # QWidget.__init__(self, parent,
        #                  Qt_WindowFlags_flags=Qt.FramelessWindowHint | Qt.Window | Qt.WindowStaysOnTopHint)
        super().__init__()

        self.find_and_compare()
        self.pixmap = QPixmap(self.size())
        self.paintPixmap()

    def find_and_compare(self):
        hwnd = win32gui.FindWindow(self.IpClassName, self.IpName)
        if not hwnd:
            print(RED, 'window not found!', DEFAULT)
            # print(hwnd)
            # hwnd = 918912

        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)  # 强行显示界面后才好截图,SW_RESTORE初始大小
        win32gui.SetForegroundWindow(hwnd)  # 将窗口提到最前
        # 裁剪得到全图
        game_rect = win32gui.GetWindowRect(hwnd)
        # src_image = ImageGrab.grab(game_rect)
        src_image = ImageGrab.grab((
        game_rect[0] + self.ANCHOR_LEFT_X, game_rect[1] + self.ANCHOR_Y, game_rect[0] + self.ANCHOR_LEFT_X + self.WIDTH,
        game_rect[1] + self.ANCHOR_Y + self.HEIGHT))
        # src_image.show()
        # 分别裁剪左右内容图片
        left_box = (0, 0, self.WIDTH // 2, self.HEIGHT)
        right_box = (self.WIDTH // 2, 0, self.WIDTH, self.HEIGHT)
        image_left = src_image.crop(left_box)
        image_right = src_image.crop(right_box)
        # image_left.show()
        # image_right.show()



        # 将左右大图裁剪成多个小图分别进行对比
        clip_mat_size = (self.WIDTH // self.CLIP_WIDTH, self.HEIGHT // self.CLIP_HEIGHT)
        self.result = zeros(clip_mat_size)
        for col in range(0, clip_mat_size[0]):
            for row in range(0, clip_mat_size[1]):
                clip_box = (col * self.CLIP_WIDTH, row * self.CLIP_HEIGHT, (col + 1) * self.CLIP_WIDTH,
                            (row + 1) * self.CLIP_HEIGHT)
                clip_image_left = image_left.crop(clip_box)
                clip_image_right = image_right.crop(clip_box)
                clip_diff = self.image_compare(clip_image_left, clip_image_right)
                if sum(clip_diff) > self.DIFF_LIMIT:
                    self.result[row][col] = 1

    def paintPixmap(self):
        # 重置遮罩图像
        self.pixmap.fill()

        # 创建绘制用的QPainter，笔画粗细为2像素
        # 事先已经在Qt窗体上铺了一个蓝色的背景图片，因此投过遮罩图案看下去标记线条是蓝色的
        p = QPainter(self.pixmap)
        p.setPen(QPen(QBrush(QColor(0, 0, 0)), 2))

        for row in range(self.result.shape[0]):
            for col in range(self.result.shape[1]):
                if self.result[row][col] != 0:
                    # 定一个基点，避免算数太难看
                    base_l_x = self.ANCHOR_LEFT_X + self.CLIP_WIDTH * col
                    base_r_x = self.ANCHOR_RIGHT_X + self.CLIP_WIDTH * col
                    base_y = self.ANCHOR_Y + self.CLIP_HEIGHT * row

                    if row == 0 or self.result[row - 1][col] == 0:
                        # 如果是第一行，或者上面的格子为空，画一条上边
                        p.drawLine(base_l_x, base_y, base_l_x + self.CLIP_WIDTH, base_y)
                        p.drawLine(base_r_x, base_y, base_r_x + self.CLIP_WIDTH, base_y)
                    if row == len(self.result) - 1 or self.result[row + 1][col] == 0:
                        # 如果是最后一行，或者下面的格子为空，画一条下边
                        p.drawLine(base_l_x, base_y + self.CLIP_HEIGHT, base_l_x + self.CLIP_WIDTH,
                                   base_y + self.CLIP_HEIGHT)
                        p.drawLine(base_r_x, base_y + self.CLIP_HEIGHT, base_r_x + self.CLIP_WIDTH,
                                   base_y + self.CLIP_HEIGHT)
                    if col == 0 or self.result[row][col - 1] == 0:
                        # 如果是第一列，或者左边的格子为空，画一条左边
                        p.drawLine(base_l_x, base_y, base_l_x, base_y + self.CLIP_HEIGHT)
                        p.drawLine(base_r_x, base_y, base_r_x, base_y + self.CLIP_HEIGHT)
                    if col == len(self.result[0]) - 1 or self.result[row][col + 1] == 0:
                        # 如果是第一列，或者右边的格子为空，画一条右边
                        p.drawLine(base_l_x + self.CLIP_WIDTH, base_y, base_l_x + self.CLIP_WIDTH,
                                   base_y + self.CLIP_HEIGHT)
                        p.drawLine(base_r_x + self.CLIP_WIDTH, base_y, base_r_x + self.CLIP_WIDTH,
                                   base_y + self.CLIP_HEIGHT)

        # 在遮罩上绘制按钮区域，避免按钮被遮罩挡住看不见
        p.fillRect(self.btn_compare.geometry(), QBrush(QColor(0, 0, 0)))
        p.fillRect(self.btn_toggle.geometry(), QBrush(QColor(0, 0, 0)))

        # 将遮罩图像作为遮罩
        self.setMask(QBitmap(self.pixmap))

    def channel_compare(self, cha_a, cha_b):
        '''
        比较两个颜色通道的差异值并返回
        '''
        sum_a = sum([i * v for i, v in enumerate(cha_a)])
        sum_b = sum([i * v for i, v in enumerate(cha_b)])
        # red_a = 0
        # red_b = 0
        # for i in range(0, 256):
        # red_a += histogram_a[i + 0] * i
        # red_b += histogram_b[i + 0] * i
        diff_channel = 0
        if sum_a + sum_b > 0:
            diff_channel = abs(sum_a - sum_b) * 10000 / max(sum_a, sum_b)
        return diff_channel

    def image_compare(self, image_a, image_b):
        '''
        返回两图的差异值, 返回两图红绿蓝差值万分比之和
        '''
        histogram_a = image_a.histogram()
        histogram_b = image_b.histogram()
        if len(histogram_a) != 768 or len(histogram_b) != 768:
            print(RED, "get histogram error", DEFAULT)
            return None
        diff_red = self.channel_compare(histogram_a[:256], histogram_b[:256])
        diff_green = self.channel_compare(histogram_a[256:512], histogram_b[256:512])
        diff_blue = self.channel_compare(histogram_a[512:768], histogram_b[512:768])
        return diff_red, diff_green, diff_blue


app = QApplication(sys.argv)
pick_hole = PickHoles()
