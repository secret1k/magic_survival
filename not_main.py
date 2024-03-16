import random
import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter, QColor, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QDesktopWidget
from PyQt5.QtCore import Qt, QTimer, QRect


class MovingObjects(QGraphicsRectItem):
    def __init__(self, object_type, hp, step, pos_x, pos_y, size_x, size_y):
        super().__init__()
        self.object_type = object_type
        self.hp = hp
        self.step = step
        self.x = pos_x
        self.y = pos_y
        self.size_x = size_x
        self.size_y = size_y
        self.move_direction_U = 0
        self.move_direction_D = 0
        self.move_direction_L = 0
        self.move_direction_R = 0

    def move_character(self):
        if self.x - self.step < 0:
            self.x = 0
        elif self.move_direction_L == 1:
            self.x -= self.step

        if self.x + self.step > 800 - self.size_x:
            self.x = 800 - self.size_x
        elif self.move_direction_R == 1:
            self.x += self.step

        if self.y - self.step < 0:
            self.y = 0
        elif self.move_direction_U == 1:
            self.y -= self.step

        if self.y + self.step > 800 - self.size_y:
            self.y = 800 - self.size_y
        elif self.move_direction_D == 1:
            self.y += self.step

    def move_enemy(self):
        if self.x > self..x:
            self.x -= self.step

    def keyPressEvent(self, event):
        if event.text() in ['Ц', 'ц', 'W', 'w']:
            self.move_direction_U = 1

        elif event.text() in ['Ф', 'ф', 'A', 'a']:
            self.move_direction_L = 1

        elif event.text() in ['Ы', 'ы', 'S', 's']:
            self.move_direction_D = 1

        elif event.text() in ['В', 'в', 'D', 'd']:
            self.move_direction_R = 1

    def keyReleaseEvent(self, event):
        if event.text() in ['Ц', 'ц', 'W', 'w']:
            self.move_direction_U = 0

        elif event.text() in ['Ф', 'ф', 'A', 'a']:
            self.move_direction_L = 0

        elif event.text() in ['Ы', 'ы', 'S', 's']:
            self.move_direction_D = 0

        elif event.text() in ['В', 'в', 'D', 'd']:
            self.move_direction_R = 0


class Game(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        self.w = self.width()
        self.h = self.height()

        self.setGeometry(30, 60, 800, 800)
        self.show()

        self.hidden_character = MovingObjects(1, 20, 5, 0, 0, 50, 50)
        self.character = MovingObjects(1, 20, 5, (self.w // 2), (self.h // 2), 50, 50)
        self.enemy = MovingObjects(2, 20, 4, 10, 10, 50, 50)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(16)

    def update_game(self):

        self.character.move_character()
        self.update()


    def keyPressEvent(self, event):
        self.character.keyPressEvent(event)

    def keyReleaseEvent(self, event):
        self.character.keyReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.character.x, self.character.y, self.character.size_x, self.character.size_y,
                         QColor(10, 10, 150))

    def resizeEvent(self, event):  # измените размер окна
        print("Окно изменено")
        QtWidgets.QMainWindow.resizeEvent(self, event)

        self.width = self.width()
        self.height = self.height()

        print(self.width, self.height)  # актуальные размеры окна

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    sys.exit(app.exec_())