import random

_start = [0, 0, 0, 0]  # человек, коза, капуста, волк
_goal = [1, 1, 1, 1]  # 0 - левый берег, 1 - правый берег
current = _start.copy()
states = [current.copy()]


def check(cur, moved_item):
    lose_conditions = [
        [0, 1, 1, 0],  # человек на левом, коза и капуста на правом
        [1, 0, 0, 1],  # человек на правом, коза и капуста на левом
        [0, 1, 0, 1],  # человек на левом, коза и волк на правом
        [1, 0, 1, 0]  # человек на правом, коза и волк на левом
    ]

    if cur in lose_conditions:
        print(f"You lose! Invalid state: {cur}")
        return False

    if cur not in states:
        states.append(cur.copy())
        print(f"New state: {cur}")
    return True


while current != _goal:
    # Выбираем что перевозим (1-коза, 2-капуста, 3-волк)
    item_to_move = random.randint(1, 3)

    # Меняем позицию человека и выбранного предмета
    if current[0] == 0:
        # Перевозим на правый берег
        new_state = current.copy()
        new_state[0] = 1
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
        print("Restarting game...")
        continue

# После выхода из цикла добавляем конечное состояние
if current == _goal and current not in states:
    states.append(current.copy())

print("\nAll states:")
for i, state in enumerate(states):
    print(f"{i}: {state}")

print("\nFinal state:", current)
print("You win!")