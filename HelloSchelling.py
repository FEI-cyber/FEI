import numpy as np
from matplotlib import pyplot as plt

# headline
SIZE = 30
THRESHOLD = 4
STEP = 20

scene = plt.figure(figsize=(10, 10), facecolor="white")
ax = scene.add_subplot(111)
plt.xlim([0, SIZE])
plt.ylim([0, SIZE])
COLORS = ("blue", "white", "red")
plt.ion()


# functions
def randomArray(size):
    list = np.random.random_integers(-1, 1, size ** 2)
    return np.reshape(list, (size, size))


def draw(array, size=SIZE, clear=True):
    if clear:
        plt.cla()
    for i in range(size):
        for j in range(size):
            ax.add_patch(
                plt.Rectangle(
                    (i, j),
                    1,
                    1,
                    color=COLORS[array[i][j] + 1],
                    alpha=0.25
                )
            )
    plt.pause(5)


def scan(array, size=SIZE):
    balance = True
    for agentX in range(size):
        for agentY in range(size):
            agent = array[agentX][agentY]
            isSatisfy, current = isSatisfied(array, agent, agentX, agentY)
            if agent == 0:
                continue
            elif isSatisfy == 1:
                continue
            else:
                # print("(" + str(agentX) + "," + str(agentY) + ") is not satisfied")
                array, moved = move(array, agentX, agentY, current)
                balance = balance & (~moved)
    return array, balance


def isSatisfied(array, agent, centerX, centerY, threshold=THRESHOLD, size=SIZE):
    similarCnt = 0
    for x in range(centerX - 1, centerX + 2):
        if (x < 0) | (x >= size):
            continue
        for y in range(centerY - 1, centerY + 2):
            if (y < 0) | (y >= size):
                continue
            if (x == centerX) & (y == centerY):
                continue
            if array[x][y] == agent:
                similarCnt += 1
    if similarCnt >= threshold:
        # print("find!")
        return 1, similarCnt
    return -1, similarCnt


def move(array, agentX, agentY, current, size=SIZE):
    moved = False
    for x in range(size):
        if moved:
            break
        for y in range(size):
            if array[x][y] != 0:
                continue
            else:
                isSatisfy, target = isSatisfied(array, array[agentX][agentY], x, y)
                if (isSatisfy == 1) | (target > current):
                    # print("(" + str(agentX) + "," + str(agentY) + ") find new home")
                    array[x][y] = array[agentX][agentY]
                    array[agentX][agentY] = 0
                    moved = True
                    break
                else:
                    continue
    return array, moved


# main
array = randomArray(SIZE)
print(array)
draw(array, clear=False)
for step in range(STEP):
    array, balance = scan(array)
    draw(array, SIZE)
    print(step)
    if balance:
        print("Balanced at step:" + str(step))
        break
plt.ioff()
plt.show()
