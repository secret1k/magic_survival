import random
import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter, QColor, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QDesktopWidget
from PyQt5.QtCore import Qt, QTimer, QRect


class Character(QGraphicsRectItem):
    def __init__(self, hp, step, pos_x, pos_y, size_x, size_y):
        super().__init__()
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

    def move(self):
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


class Enemy:
    def __init__(self, hp, step, pos_x, pos_y, size_x, size_y):
        spawn_x_or_y = random.randint(0, 3)
        if spawn_x_or_y == 0:
            self.y = -30
            self.x = random.randint(-10, 800)
        elif spawn_x_or_y == 1:
            self.y = 800
            self.x = random.randint(-10, 800)
        elif spawn_x_or_y == 2:
            self.x = -30
            self.y = random.randint(-10, 800)
        elif spawn_x_or_y == 3:
            self.x = 800
            self.y = random.randint(-10, 800)
        self.hp = hp
        self.step = step
        self.pos_x = self.x
        self.pos_y = self.y
        self.size_x = size_x
        self.size_y = size_y

    # def move(self):
    #     if self.x > Character.x:
    #         self.x -= self.step
    #     if self.x < Character.x:
    #         self.x += self.step
    #     if self.y > Character.y:
    #         self.y -= self.step
    #     if self.y < Character.y:
    #         self.y += self.step
    #     if self.collidesWithItem(self.character):
    #         print("Character got hit!")


class Game(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        self.w = self.size().width()
        self.h = self.size().height()

        self.setGeometry(30, 60, 800, 800)
        self.show()

        self.hidden_character = Character(20, 5, 0, 0, 50, 50)
        self.character = Character(20, 5, (self.w // 2), (self.h // 2), 50, 50)

        self.enemy = Enemy(20, 4, 10, 10, 30, 30)
        self.enemies = []
        self.enemy_timer = QTimer()
        self.enemy_timer.timeout.connect(self.create_enemy)
        self.enemy_timer.start(1000)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(16)

    def update_game(self):

        self.character.move()

        for enemy in self.enemies:
            if enemy.x > self.character.x:
                enemy.x -= enemy.step
            if enemy.x < self.character.x:
                enemy.x += enemy.step

            if enemy.y > self.character.y:
                enemy.y -= enemy.step
            if enemy.y < self.character.y:
                enemy.y += enemy.step
        #if self.enemy.collidesWithItem(self.character):
        #   print("Character got hit!")

        self.update()


    def keyPressEvent(self, event):
        self.character.keyPressEvent(event)

    def keyReleaseEvent(self, event):
        self.character.keyReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.character.x, self.character.y, self.character.size_x, self.character.size_y,
                         QColor(10, 10, 150))
        for enemy in self.enemies:
            painter.drawImage(QRect(enemy.x, enemy.y, 30, 30), QImage('enemy.jpg'))
            # painter.fillRect(self.enemy.x, self.enemy.y, self.enemy.size_x, self.enemy.size_y, QColor(150, 150, 10))

    def create_enemy(self):
        enemy = Enemy(20, 1, 0, 0, 30, 30)
        self.enemies.append(enemy)

    def resizeEvent(self, event):  # измените размер окна
        print("Окно изменено")
        QtWidgets.QMainWindow.resizeEvent(self, event)

        self.size().width = self.width()
        self.size().height = self.height()

        print(self.width, self.height)  # актуальные размеры окна

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    sys.exit(app.exec_())