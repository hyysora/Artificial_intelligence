from keras.saving.save import load_model
import numpy as np
import cv2 as cv
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QPixmap, QPen
from PyQt5.QtCore import Qt, QPoint

img_path = "hand_draw.jpg"
model = load_model('hand_write.h5')
model.summary()


class Winform(QWidget):
    def __init__(self, parent=None):
        super(Winform, self).__init__(parent)
        self.setWindowTitle("绘图判断数字")
        self.pix = QPixmap()
        self.lastPoint = QPoint()
        self.endPoint = QPoint()
        self.init_Ui()

    def init_Ui(self):
        self.setFixedSize(600, 500)

        self.pix = QPixmap(500, 500)
        self.pix.fill(Qt.black)

        self.off_set = QPoint(self.width() - self.pix.width(), self.height() - self.pix.height())

        btn_clear = QPushButton(self)
        btn_clear.setText("清空")
        btn_clear.resize(80, 30)
        btn_clear.move(10, 30)
        btn_clear.clicked.connect(self.clear)

        btn_save = QPushButton(self)
        btn_save.setText("判断")
        btn_save.resize(80, 30)
        btn_save.move(10, 80)
        btn_save.clicked.connect(self.save)

        btn_open = QPushButton(self)
        btn_open.setText("打开")
        btn_open.resize(80, 30)
        btn_open.move(10, 130)
        btn_open.clicked.connect(self.open)

    def clear(self):
        self.pix.fill(Qt.black)
        self.update()

    def save(self):
        self.pix.save(img_path)
        img_read = cv.imread(img_path)
        img = cv.cvtColor(img_read, cv.COLOR_RGB2GRAY)
        img = cv.resize(img, (28, 28))
        y_pred = model.predict(img.reshape((1, 784)))
        QMessageBox.about(self, "数字是", str(np.argmax(y_pred, axis=1)))

    def open(self):
        img_name, img_type = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
        jpg = QPixmap(img_name).scaled(self.pix.width(), self.pix.height())
        if not jpg.isNull():
            self.pix = jpg

    def paintEvent(self, event):
        pp = QPainter(self.pix)
        pen = QPen()
        pen.setWidth(30)
        pen.setColor(Qt.white)
        pp.setPen(pen)
        pp.drawLine(self.lastPoint, self.endPoint)
        self.lastPoint = self.endPoint
        painter = QPainter(self)
        painter.drawPixmap(100, 0, self.pix)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.lastPoint = event.pos() - self.off_set
            self.endPoint = self.lastPoint

    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton:
            self.endPoint = event.pos() - self.off_set
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.endPoint = event.pos() - self.off_set
            self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Winform()
    form.show()
    sys.exit(app.exec_())
