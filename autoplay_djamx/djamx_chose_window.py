import sys
import time
import cv2
import numpy as np
import win32con
import win32gui
from PIL import ImageGrab
from PyQt5.QtWidgets import *

hwnd_title = dict()


def get_all_hwnd(hwnd, mouse):
    if win32gui.IsWindow(hwnd) \
            and win32gui.IsWindowEnabled(hwnd) \
            and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})


class MyWindow(QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setWindowTitle("选择训练窗口")
        self.resize(400, 200)
        layout = QVBoxLayout()

        win32gui.EnumWindows(get_all_hwnd, 0)
        for h, t in hwnd_title.items():
            if t != "":
                self.btn = QPushButton(self)
                self.btn.setText(t)
                self.btn.setWindowTitle(str(h))
                self.btn.clicked.connect(self.msg)
                layout.addWidget(self.btn)

        self.setLayout(layout)

    def msg(self):
        title = self.sender().text()
        answer = QMessageBox.information(self, "DQN训练", "是否开始训练：" + title,
                                         QMessageBox.Yes | QMessageBox.No)
        if answer == QMessageBox.Yes:
            print('start')
            h = self.sender().windowTitle()
            win_h = int(h)
            win32gui.ShowWindow(win_h, win32con.SW_RESTORE)  # 强行显示界面后才好截图
            win32gui.SetForegroundWindow(win_h)  # 将窗口提到最前
            time.sleep(1)
            flag = False
            while True:
                left, top, right, bot = win32gui.GetWindowRect(win_h)
                screen = np.array(ImageGrab.grab(bbox=(left, top, right, bot)))
                if flag:
                    img = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
                    cv2.imshow('window', img)
                    print(img)
                else:
                    img = cv2.Canny(cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY), threshold1=200, threshold2=300)
                    cv2.imshow('window', img)
                    print(img)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break
        else:
            print('end')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())
