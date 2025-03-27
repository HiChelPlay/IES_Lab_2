import random

_start = [0,0,0,0] #человек, коза, капуста, волк
_goal = [1,1,1,1]  #0 - левый берег, 1 - правый берег
current = _start

# o1 = [1, 0 -> 1, 0 -> 1, 0 -> 1]
# o2 = [0, 1 -> 0, 1 -> 0, 1 -> 0]

states = [current.copy()]

def check(cur, a):
    lose_conditions = [
        [0,1,1,0], [0,1,1,1],
        [0,1,0,1], [0,1,1,1],
        [1,0,0,0], [1,0,1,0],
        [1,0,0,1], [1,0,0,0]
    ]
    if cur in lose_conditions:
        print("You lose!")
        if cur[0] == 0:
            cur[0] = 1
            cur[a] = 1
        else:
            cur[0] = 0
            cur[a] = 0

        return False
    else:
        # Добавляем копию состояния
        if cur not in states:
            states.append(cur.copy())
            print(cur)
        return True


while current != _goal:
    while current != _goal:
        if current[0] == 0:
            current[0] = 1
            i = random.randint(0, 3)
            current[i] = 1
        else:
            current[0] = 0
            i = random.randint(0, 3)
            current[i] = 0

        print(current)

        # Проверяем состояние
        check(current, i)



print(states)
print(current)

print("You win!")
