import sys

from PyQt6.QtCore import QRectF, Qt
# from PyQt6.QtGui import QPixmap, QPen, QBrush, QColor
from PyQt6.QtGui import *
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, \
    QGraphicsProxyWidget


class Scene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setSceneRect(0, 0, 800, 450)
        rect_with_size_like_bg = self.addRect(QRectF(0, 0, self.width(), self.height()), QPen(Qt.PenStyle.NoPen),
                                              QBrush(QColor(60, 0, 40)))


class View(QGraphicsView):
    def __init__(self, scene):
        super().__init__()

        self.setScene(scene)
        self.setMinimumSize(400, 225)
        self.setMaximumSize(1600, 900)
        self.move(50, 50)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setStyleSheet('border: none;')

    def resizeEvent(self, event):
        self.fitInView(QRectF(0, 0, 800, 450), Qt.AspectRatioMode.KeepAspectRatio)


# class Entity():
#     def __init__(self):


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Scene()
    game_window = View(game)
    game_window.show()
    sys.exit(app.exec())
