import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QDesktopWidget
from PyQt5.QtCore import Qt, QTimer

class Character(QGraphicsRectItem):
    def __init__(self):
        super().__init__(0, 0, 50, 50)
        # self.setBrush(Qt.blue)
        # self.setFlag(QGraphicsRectItem.ItemIsFocusable)
        self.setFocus()
        self.step = 5
        self.X_SIZE_PLAYER = 50
        self.Y_SIZE_PLAYER = 50
        self.move_direction_U = 0
        self.move_direction_D = 0
        self.move_direction_L = 0
        self.move_direction_R = 0
        self.x = 0  # current position
        self.y = 0  # current position

    def move(self):
        if self.x - self.step < 0:
            self.x = 0

        elif self.move_direction_L == 1:
            self.x -= self.step

        if self.x + self.step > 800 - self.X_SIZE_PLAYER:
            self.x = 800 - self.X_SIZE_PLAYER
        elif self.move_direction_R == 1:
            self.x += self.step

        if self.y - self.step < 0:
            self.y = 0
        elif self.move_direction_U == 1:
            self.y -= self.step

        if self.y + self.step > 800 - self.Y_SIZE_PLAYER:
            self.y = 800 - self.Y_SIZE_PLAYER
        elif self.move_direction_D == 1:
            self.y += self.step

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


class Enemy(QGraphicsRectItem):
    def __init__(self, character):
        super().__init__(0, 0, 30, 30)
        self.setBrush(Qt.red)
        self.setPos(400, 300)
        self.character = character

    def move(self):
        step = 0.5
        if self.x() > self.character.x():
            self.moveBy(-step, 0)
        else:
            self.moveBy(step, 0)
        if self.y() > self.character.y():
            self.moveBy(0, -step)
        else:
            self.moveBy(0, step)
        if self.collidesWithItem(self.character):
            print("Character got hit!")


class Game(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        self.w = self.size().width()
        self.h = self.size().height()

        self.setGeometry(30, 30, 800, 800)
        self.show()
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)

        self.character = Character()

        # self.character.setPos(self.width() / 2 - self.character.rect().width() / 2,
        #                       self.height() / 2 - self.character.rect().height() / 2)
        # self.scene.addItem(self.character)

        # self.enemy = Enemy(self.character)
        # self.scene.addItem(self.enemy)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(16)

    def update_game(self):
        self.character.move()
        self.update()


    def keyPressEvent(self, event):
        self.character.keyPressEvent(event)

    def keyReleaseEvent(self, event):
        self.character.keyReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.character.x, self.character.y, self.character.X_SIZE_PLAYER, self.character.Y_SIZE_PLAYER,
                         QColor(10, 10, 150))

    def resizeEvent(self, event):  # измените размер окна
        print("Окно изменено")
        QtWidgets.QMainWindow.resizeEvent(self, event)

        self.width = self.size().width()
        self.height = self.size().height()

        print(self.width, self.height)  # актуальные размеры окна


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    sys.exit(app.exec_())
