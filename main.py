
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsRectItem
from PyQt5.QtCore import Qt, QTimer


class Character(QGraphicsRectItem):
    def __init__(self):
        super().__init__(0, 0, 50, 50)
        self.setBrush(Qt.blue)
        self.setFlag(QGraphicsRectItem.ItemIsFocusable)
        self.setFocus()
        self.step = 1
        self.move_directions = set()
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.move)
        self.animation_timer.start(10)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_W:
            self.move_directions.add("up")
        elif event.key() == Qt.Key_S:
            self.move_directions.add("down")
        elif event.key() == Qt.Key_A:
            self.move_directions.add("left")
        elif event.key() == Qt.Key_D:
            self.move_directions.add("right")

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_W:
            self.move_directions.discard("up")
        elif event.key() == Qt.Key_S:
            self.move_directions.discard("down")
        elif event.key() == Qt.Key_A:
            self.move_directions.discard("left")
        elif event.key() == Qt.Key_D:
            self.move_directions.discard("right")

    def move(self):
        if "up" in self.move_directions:
            self.moveBy(0, -self.step)
        if "down" in self.move_directions:
            self.moveBy(0, self.step)
        if "left" in self.move_directions:
            self.moveBy(-self.step, 0)
        if "right" in self.move_directions:
            self.moveBy(self.step, 0)


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
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)
        self.character = Character()
        self.scene.addItem(self.character)
        self.enemy = Enemy(self.character)
        self.scene.addItem(self.enemy)

        self.timer = QTimer()
        self.timer.timeout.connect(self.enemy.move)
        self.timer.start(10)

    def keyPressEvent(self, event):
        self.character.keyPressEvent(event)

    def keyReleaseEvent(self, event):
        self.character.keyReleaseEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    game.show()
    sys.exit(app.exec_())
