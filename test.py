import sys
from time import sleep

from PySide6.QtWidgets import (QApplication, QMainWindow, QMessageBox)
from PySide6.QtCore import QRect
from PySide6.QtGui import QStandardItemModel, QStandardItem


import random

from int import Ui_MainWindow

_start = [0, 0, 0, 0]  # человек, коза, капуста, волк
_goal = [1, 1, 1, 1]  # 0 - левый берег, 1 - правый берег
current = _start.copy()
states = [current.copy()]


def check(cur, moved_item):
    lose_conditions = [
        [0,1,1,0], [0,1,1,1],
        [0,1,0,1], [0,1,1,1],
        [1,0,0,0], [1,0,1,0],
        [1,0,0,1], [1,0,0,0]
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

print("\nAll states:")
for i, state in enumerate(states):
    print(f"{i}: {state}")

print("\nFinal state:", current)
print("You win!")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Создание UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Подключение сигналов
        self.ui.pushButton.clicked.connect(self.button_clicked)


    goatPos = 100
    def button_clicked(self):
        for i, state in enumerate(states):
            goatPos = self.ui.label_2.pos().x()
            if state[3] == 1:
                self.ui.label_2.setGeometry(QRect(330, 290, 71, 81))
            else:
                self.ui.label_2.setGeometry(QRect(100, 290, 71, 81))
            sleep(0.2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())