
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QDesktopWidget
from PyQt5.QtCore import Qt, QTimer



class Character(QGraphicsRectItem):
    def __init__(self):
        super().__init__(0, 0, 1, 1)
        self.setBrush(Qt.blue)
        self.setFlag(QGraphicsRectItem.ItemIsFocusable)
        self.setFocus()
        self.step = 4
        self.move_directions = set()
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.move)
        self.animation_timer.start(10)


    def keyPressEvent(self, event):
        if event.text() in ['w','W','ц','Ц']:
            self.move_directions.add("up")
        elif event.text() in ['s','S','ы','Ы']:
            self.move_directions.add("down")
        elif event.text() in ['a','A','ф','Ф']:
            self.move_directions.add("left")
        elif event.text() in ['d','D','в','В']:
            self.move_directions.add("right")

    def keyReleaseEvent(self, event):
        if event.text() in ['w','W','ц','Ц']:
            self.move_directions.discard("up")
        elif event.text() in ['s','S','ы','Ы']:
            self.move_directions.discard("down")
        elif event.text() in ['a','A','ф','Ф']:
            self.move_directions.discard("left")
        elif event.text() in ['d','D','в','В']:
            self.move_directions.discard("right")

    def move(self):
        current_pos = self.scenePos()
        new_pos = current_pos
        scene_rect = self.scene().sceneRect()

        if "up" in self.move_directions:
            new_pos.setY(current_pos.y() - self.step)
        if "down" in self.move_directions:
            new_pos.setY(current_pos.y() + self.step)
        if "left" in self.move_directions:
            new_pos.setX(current_pos.x() - self.step)
        if "right" in self.move_directions:
            new_pos.setX(current_pos.x() + self.step)

        scene_rect = self.scene().sceneRect()
        if not scene_rect.contains(new_pos):
            new_pos.setX(max(scene_rect.left(), min(new_pos.x(), scene_rect.right() - self.rect().width())))
            new_pos.setY(max(scene_rect.top(), min(new_pos.y(), scene_rect.bottom() - self.rect().height())))

        self.setPos(new_pos)

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
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setWindowState(Qt.WindowFullScreen)
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        screen_rect = QDesktopWidget().screenGeometry()
        #self.setSceneRect(screen_rect)
        #self.view.fitInView(self.sceneRect(), Qt.KeepAspectRatio)

        self.setCentralWidget(self.view)
        self.character = Character()
        self.character.setPos(self.width() / 2 - self.character.rect().width() / 2,
                              self.height() / 2 - self.character.rect().height() / 2)
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
    game.showFullScreen()  # Отображение окна на весь экран
    sys.exit(app.exec_())