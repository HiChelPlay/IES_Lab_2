import sys
from time import sleep

from PySide6.QtWidgets import (QApplication, QMainWindow, QMessageBox)
from PySide6.QtCore import QRect, QTimer
from PySide6.QtGui import QStandardItemModel, QStandardItem, QTransform, QPixmap

import random

from int import Ui_MainWindow

_start = [0, 0, 0, 0]  # человек, коза, капуста, волк
_goal = [1, 1, 1, 1]  # 0 - левый берег, 1 - правый берег
current = _start.copy()
states = [current.copy()]


def check(cur, moved_item):
    lose_conditions = [
        [0, 1, 1, 0], [0, 1, 1, 1],
        [0, 1, 0, 1], [0, 1, 1, 1],
        [1, 0, 0, 0], [1, 0, 1, 0],
        [1, 0, 0, 1], [1, 0, 0, 0]
    ]

    if cur in lose_conditions:
        return False

    if cur not in states:
        states.append(cur.copy())
    return True


while current != _goal:
    # Выбираем что перевозим (1-коза, 2-капуста, 3-волк)
    item_to_move = random.randint(1, 3)

    # Меняем позицию человека и выбранного предмета
    if current[0] == 0:
        # Перевозим на правый берег
        new_state = current.copy()
        new_state[0] = 1
        if random.random() < 0.5:
            new_state[item_to_move] = 1
    else:
        # Возвращаемся на левый берег (можем взять или не взять предмет)
        new_state = current.copy()
        new_state[0] = 0
        # С 50% вероятностью берём предмет обратно
        if random.random() < 0.5:
            new_state[item_to_move] = 0

    # Проверяем новое состояние
    if check(new_state, item_to_move):
        current = new_state.copy()
    else:
        # При проигрыше начинаем заново
        current = _start.copy()
        states = [current.copy()]
        continue

# После выхода из цикла добавляем конечное состояние
if current == _goal and current not in states:
    states.append(current.copy())



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Создание UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Подключение сигналов
        self.ui.pushButton.clicked.connect(self.button_clicked)

        # Таймер для последовательного перемещения
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_position)
        self.current_state_index = 0

    def button_clicked(self):
        self.current_state_index = 0
        self.timer.start(500)  # 500 ms = 0.5 секунды
        self.ui.textEdit.setText('Человек\tКоза\tКапуста\tВолк\n\n')


    def update_position(self):
        if self.current_state_index < len(states):

            state = states[self.current_state_index]
            nameState = []
            for i in state:
                if i == 0:
                    nameState.append("Левый")
                else:
                    nameState.append("Правый")
            curTxt = self.ui.textEdit.toPlainText()
            for i in nameState:
                newTxt = curTxt + f'{i}\t'
                curTxt = newTxt
            newTxt = f'{newTxt}\n'
            self.ui.textEdit.setText(newTxt)

            #перемещение лодки и человека
            if state[0] == 1 and self.ui.boat.geometry().x() == 180:
                self.ui.boat.move(270, self.ui.boat.geometry().y())
                self.ui.man.move(430, self.ui.man.geometry().y())
                pixmap = self.ui.boat.pixmap()
                if pixmap:
                    mirrored = pixmap.transformed(QTransform().scale(-1, 1))
                    self.ui.boat.setPixmap(mirrored)
                pixmap = self.ui.man.pixmap()
                if pixmap:
                    mirrored = pixmap.transformed(QTransform().scale(-1, 1))
                    self.ui.man.setPixmap(mirrored)
            elif state[0] == 0 and self.ui.boat.geometry().x() == 270:
                self.ui.boat.move(180, self.ui.boat.geometry().y())
                self.ui.man.move(100, self.ui.man.geometry().y())
                pixmap = self.ui.boat.pixmap()
                if pixmap:
                    mirrored = pixmap.transformed(QTransform().scale(-1, 1))
                    self.ui.boat.setPixmap(mirrored)
                pixmap = self.ui.man.pixmap()
                if pixmap:
                    mirrored = pixmap.transformed(QTransform().scale(-1, 1))
                    self.ui.man.setPixmap(mirrored)


            #перемещение остальных
            list = ['', self.ui.goat, self.ui.cabbage, self.ui.wolf]

            for i, cur in enumerate(list):
                if i != 0:
                    if state[i] == 1:
                        pixmap = cur.pixmap()
                        if pixmap and cur.geometry().x() == 100:
                            mirrored = pixmap.transformed(QTransform().scale(-1, 1))
                            cur.setPixmap(mirrored)

                        # self.ui.goat.setGeometry(QRect(330, 290, 71, 81))
                        cur.move(430, cur.geometry().y())
                    else:
                        pixmap = cur.pixmap()
                        if pixmap and cur.geometry().x() == 430:
                            mirrored = pixmap.transformed(QTransform().scale(-1, 1))
                            cur.setPixmap(mirrored)
                        # self.ui.goat.setGeometry(QRect(100, 290, 71, 81))
                        cur.move(100, cur.geometry().y())

            self.current_state_index += 1
        else:
            self.timer.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())