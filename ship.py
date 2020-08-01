from random import randint
from time import sleep


class Field:
    def __init__(self):
        pass



    def CreateField(self, x, y):
        self.field = [[i - 1 if (j == 0 and i != 0) else "#" for i in range(x)] for j in range(y)]
        for i in range(1, y):
            self.field[i][0] = i - 1
        self.field[0][0] = " "

        return self.field



class MyField(Field):
    def __init__(self, x, y, n):
        self.num = n
        self.x = x
        self.y = y
        self.field = self.CreateField(x, y)



    def GetField(self):
        return self.field



    def SetRightShip(self, lvl, y, x):
        flag = 0
        area = [[] for i in range(3)]
        for i in range(-1, 2):
            for j in range(-1, lvl + 1):

                try:
                    cell = self.field[y + i][x + j]
                except:
                    continue

                if cell != "#" and cell != "∆": continue
                try:
                    if (cell == "∆"): flag = 1
                    area[i + 1].append(cell)
                except:
                    continue

        if not flag and len(area[1]) > lvl:
            for i in range(lvl):
                self.field[y][x + i] = "∆"
            return 1



    def SetDownShip(self, lvl, y, x):
        flag = 0
        area = [[] for i in range(lvl + 2)]
        for i in range(-1, lvl + 1):
            for j in range(-1, 2):

                try:
                    cell = self.field[y + i][x + j]
                except:
                    continue

                if cell != "#" and cell != "∆": continue
                try:
                    if (cell == "∆"): flag = 1
                    area[i + 1].append(cell)
                except:
                    continue
        c = 0
        for i in area:
            if len(i) > 0: c += 1

        if not flag and c > lvl:
            for i in range(lvl):
                self.field[y + i][x] = "∆"
            return 1



    def SetShip(self, lvl, y, x, v):
        if v == "r":
            return self.SetRightShip(lvl, y, x)

        elif v == "d":
            return self.SetDownShip(lvl, y, x)



    def SetShips(self):
        count = 5

        if self.num != 3:
            print("\n" * 30)
            print("Player " + str(self.num) + ":")
            for i in range(self.y): print(*self.GetField()[i])

        for lvl in range(1, count):
            for ship in range(count - 1):

                while True:
                    if self.num != 3:
                        y, x, v = input("Enter y, x, vector right = r, down = d: ").split()
                    else:
                        vectors = ["r", "d"]
                        v = vectors[randint(0, 1)]
                        y = randint(0, 9)
                        x = randint(0, 9)

                    res = self.SetShip(lvl, int(y) + 1, int(x) + 1, v)

                    if not res and self.num != 3:
                        print("This is wrong place!")
                    elif res == 1:
                        break

                if self.num != 3:
                    print("\n" * 30)
                    for i in range(self.y): print(*self.GetField()[i])

            count -= 1



    def Check(self, y, x):
        if self.field[y][x] == "∆":
            return 1
        else:
            return 0


class EnemyField(Field):
    def __init__(self, y, x, n):
        self.num = n
        self.field = self.CreateField(y, x)
        self.score = 0

    def GetCellArea(self, y, x, field):
        area = []

        if field[y][x] not in "^o×":
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    try:
                        area.append(field[y + i][x + j])
                    except:
                        pass
        return area



    def TryDestroy(self, y, x, enemy):
        r = 1
        edges = []
        verticalElements = [i[x] for i in enemy.field]

        leftEdge = enemy.field[y].index("^") - 1
        edges.append(enemy.field[y][leftEdge])

        rightEdge = len(enemy.field[y]) - (list(reversed(enemy.field[y])).index("^") - 1) - 1
        if rightEdge != 11:
            edges.append(enemy.field[y][rightEdge])

        topEdge = verticalElements.index("^") - 1
        edges.append(verticalElements[topEdge])

        bottomEdge = len(verticalElements) - (list(reversed(verticalElements)).index("^") - 1) - 1
        if bottomEdge != 11:
            edges.append(verticalElements[bottomEdge])

        if not "∆" in edges:
            r = 2

            enemy.field[y][x] = "×"
            self.field[y][x] = "×"
            for i in range(leftEdge + 1, rightEdge):
                enemy.field[y][i] = "×"
                self.field[y][i] = "×"

            for i in range(topEdge + 1, bottomEdge):
                enemy.field[i][x] = "×"
                self.field[i][x] = "×"

            for i in range(1, 11):
                for j in range(1, 11):
                    area1 = self.GetCellArea(i, j, enemy.field)
                    area2 = self.GetCellArea(i, j, self.field)

                    if "×" in area1:
                        enemy.field[i][j] = "o"

                    if "×" in area2:
                        self.field[i][j] = "o"

        return r



    def Hit(self, enemy, y, x):
        y += 1
        x += 1
        res = enemy.Check(y, x)

        if res:
            self.score += 1
            enemy.field[y][x] = "^"
            self.field[y][x] = "^"

            res = self.TryDestroy(y, x, enemy)
        else:
            enemy.field[y][x] = "o"
            self.field[y][x] = "o"

        return res



class Bot():
    def __init__(self):
        self.fields = {"f": MyField(11, 11, 3), "ef": EnemyField(11, 11, 3)}

        self.fields["f"].SetShips()
        self.lasthit = 0
        self.wound_y = 0
        self.wound_x = 0

        self.v = ""
        self.streak = 0
        self.losestreak = 0



    def Is_gap_good(self, y, x, field):
        area = self.fields["ef"].GetCellArea(y + 1, x + 1, field)

        if "×" not in area and len(area) != 0:
            return 1
        return 0



    def GetValueOfCell(self, y, x):
        area = self.fields["ef"].GetCellArea(y, x, self.fields["ef"].field)

        return area.count("#")



    def FindDefaultCells(self):
        pnts = []
        max_free = -1

        for row in range(1, 11):
            for column in range(1, 11):

                val = self.GetValueOfCell(row, column)

                if val > max_free:
                    max_free = val
                    pnts = [[row - 1, column - 1]]
                elif val == max_free:
                    pnts.append([row - 1, column - 1])

        return pnts



    def FindEdgeCells(self):
        pnts = []
        max_free = -1

        for row in range(1, 11):
            for column in range(1, 11):
                if row in [1, 10] or column in [1, 10]:
                    val = self.GetValueOfCell(row, column)

                    if val > max_free:
                        max_free = val
                        pnts = [[row - 1, column - 1]]
                    elif val == max_free:
                        pnts.append([row - 1, column - 1])

        return pnts



    def GetPoint(self, enemy):
        defPoints = self.FindDefaultCells()
        edgePoints = self.FindEdgeCells()

        if self.losestreak > 3 and len(edgePoints) > 0:
            point = edgePoints[randint(0, len(edgePoints) - 1)]
        else:
            point = defPoints[randint(0, len(defPoints) - 1)]

        return point




    def FindFireVector(self, enemy):
        points = []
        if self.wound_x + 2 < 11:
            if enemy.field[self.wound_y + 1][self.wound_x + 2] not in "^o":
                if self.Is_gap_good(self.wound_y, self.wound_x + 1, enemy.field):
                    points.append([self.wound_y, self.wound_x + 1])

        if self.wound_y + 2 < 11:
            if enemy.field[self.wound_y + 2][self.wound_x + 1] not in "^o":
                if self.Is_gap_good(self.wound_y + 1, self.wound_x, enemy.field):
                    points.append([self.wound_y + 1, self.wound_x])

        if self.wound_x != 0:
            if enemy.field[self.wound_y + 1][self.wound_x] not in "^o":
                if self.Is_gap_good(self.wound_y, self.wound_x - 1, enemy.field):
                    points.append([self.wound_y, self.wound_x - 1])

        if self.wound_y != 0:
            if enemy.field[self.wound_y][self.wound_x + 1] not in "^o":
                if self.Is_gap_good(self.wound_y - 1, self.wound_x, enemy.field):
                    points.append([self.wound_y - 1, self.wound_x])

        max = -1
        point = []

        for i in points:
            weight = self.GetValueOfCell(i[0], i[1])
            if weight > max:
                point = i
                max = weight

        return point



    def FolowTheWay(self, enemy):
        if self.v == "r":
            if self.wound_x + 1 == 10 or enemy.field[self.wound_y + 1][self.wound_x + 2] == "o":
                self.v = "l"
                x = self.wound_x - self.streak
                y = self.wound_y
            else:
                y = self.wound_y
                x = self.wound_x + 1

        elif self.v == "d":
            if self.wound_y + 1 == 10 or enemy.field[self.wound_y + 2][self.wound_x + 1] == "o":
                self.v = "u"
                x = self.wound_x
                y = self.wound_y - self.streak
            else:
                y = self.wound_y + 1
                x = self.wound_x

        elif self.v == "l":
            if self.wound_x - 1 == -1 or enemy.field[self.wound_y + 1][self.wound_x] == "o":
                self.v = "r"
                x = self.wound_x + self.streak
                y = self.wound_y
            else:
                y = self.wound_y
                x = self.wound_x - 1

        elif self.v == "u":
            if self.wound_y - 1 == -1 or enemy.field[self.wound_y][self.wound_x + 1] == "o":
                self.v = "d"
                x = self.wound_x
                y = self.wound_y + self.streak
            else:
                y = self.wound_y - 1
                x = self.wound_x

        return [y, x]



    def MemorizeWoundCell(self, y, x):
        self.lasthit = 1
        self.wound_y = y
        self.wound_x = x
        self.streak += 1



    def SetShootingVector(self,y, x, enemy):
        if enemy.field[y + 1][x] == "^":
            self.v = "r"

        elif x + 2 != 11 and enemy.field[y + 1][x + 2] == "^":
            self.v = "l"

        elif y + 2 != 11 and enemy.field[y + 2][x + 1] == "^":
            self.v = "u"

        elif enemy.field[y][x + 1] == "^":
            self.v = "d"



    def NullMemory(self):
        self.lasthit = 0
        self.streak = 0
        self.losestreak = 0
        self.v = ""



    def TwistVector(self):
        if self.v == "r":
            self.v = "l"
            self.wound_x -= (self.streak - 1)

        elif self.v == "l":
            self.v = "r"
            self.wound_x += (self.streak - 1)

        elif self.v == "d":
            self.v = "u"
            self.wound_y -= (self.streak - 1)

        if self.v == "u":
            self.v = "d"
            self.wound_y += (self.streak - 1)



    def HitEnemy(self, enemy):
        if self.lasthit == 0:                                   # Find the cell to attac
            y, x = self.GetPoint(enemy)                         # If there is no wounded ship - hit random available cell

        else:                                                   # Hit available cells whose are around wounded cell to find vector of fire
            if self.v == "":
                y, x = self.FindFireVector(enemy)

            else:                                               # change vector of fire if continue is not available
                y, x = self.FolowTheWay(enemy)

        # attac
        res = self.fields["ef"].Hit(enemy, y, x)

        if res == 1:                                            # If only first hit - memorize the cell
            self.losestreak = 0
            self.MemorizeWoundCell(y, x)

            if self.streak == 2:                                # If it is second hit to ship - memorize vector of shooting
                self.SetShootingVector(y, x, enemy)

        elif res == 2:                                          # If after hit the ship is destroyed - null memory
            self.NullMemory()

        elif res == 0 and self.streak >= 2:                     # If hit is missed on vector - change vector to opposit
            self.losestreak += 1
            self.TwistVector()

        elif res == 0:
            self.losestreak += 1
            if self.losestreak > (4 + randint(1, 5)):
                self.losestreak = 0

        for i in self.fields["ef"].field:
            print(*i)

        return res



    def CheckWin(self):
        res = self.fields["ef"].score
        if res == 20:
            return 1
        else:
            return 0



class GamePlay1x1:
    def __init__(self):
        self.multicast = 1

        self.p1 = {"f": MyField(11, 11, 1), "ef": EnemyField(11, 11, 1)}
        self.p2 = {"f": MyField(11, 11, 2), "ef": EnemyField(11, 11, 2)}

        self.p1["f"].SetShips()
        self.p2["f"].SetShips()

        self.flag = 0



    def ShowFields(self, player):
        print("\n" * 30, "Player " + str(self.flag + 1) + " hits, multicast: " + str(self.multicast))
        for i in player["f"].GetField():
            print(*i)

        print("\n")
        for i in player["ef"].field:
            print(*i)



    def Atack(self, frm, to):
        while True:
            try:
                y, x = list(map(int, input("Enter y, x to hit: ").split()))
                res = frm.Hit(to, y, x)
                break
            except:
                print("Wrong!")
                continue

        return res



    def Player1Step(self):
        self.ShowFields(self.p1)

        res = self.Atack(self.p1["ef"], self.p2["f"])

        if not res:
            self.flag = 1
            self.multicast = 1
        else:
            self.multicast += 1



    def Player2Step(self):
        self.ShowFields(self.p2)

        res = self.Atack(self.p2["ef"], self.p1["f"])

        if not res:
            self.flag = 0
            self.multicast = 1
        else:
            self.multicast += 1



    def LoadNextPlayer(self):
        sec = 5
        print("Next player's map is loaded after...")
        for i in range(5):
            print(sec)
            sec -= 1
            sleep(1)



    def Start(self):
        while True:
            if not self.flag:
                self.Player1Step()

            else:
                self.Player2Step()

            if self.p1["ef"].score == 20:
                print("Player 1 won!")
                break

            elif self.p2["ef"].score == 20:
                print("Player 2 won!")
                break

            if self.multicast == 1:
                self.LoadNextPlayer()




class GamePlayWithBot():
    def __init__(self):
        self.bot = Bot()
        self.p1 = {"f": MyField(11, 11, 1), "ef": EnemyField(11, 11, 1)}
        self.p1["f"].SetShips()
        self.multicast = 1

        self.flag = 0



    def ShowFields(self):
        for i in self.p1["f"].GetField():
            print(*i)

        print("\n")

        for i in self.p1["ef"].field:
            print(*i)



    def Atack(self, frm, to):
        while True:
            try:
                y, x = list(map(int, input("Enter y, x to hit: ").split()))
                res = frm.Hit(to, y, x)
                break
            except:
                print("Wrong!")
                continue

        return  res



    def HumanStep(self):
        print("\n" * 30, "Human hits, multicast: " + str(self.multicast))
        self.ShowFields()

        res = self.Atack(self.p1["ef"], self.bot.fields["f"])

        if not res:
            self.flag = 1
            self.multicast = 1
        else:
            self.multicast += 1



    def BotStep(self):
        res = self.bot.HitEnemy(self.p1["f"])

        print("\n" * 30, "Bot hits, multicast: " + str(self.multicast))
        self.ShowFields()

        if not res:
            self.flag = 0
            self.multicast = 1
        else:
            self.multicast += 1
        sleep(2)



    def Start(self):
        while True:
            if not self.flag:
                self.HumanStep()

            else:
                self.BotStep()

            if self.p1["ef"].score == 20:
                print("Player 1 won!")
                break

            elif self.bot.CheckWin():
                print("Bot won!")
                break




def main():
    gametype = int(input("Game with friend - 1, with bot - 2: "))

    if gametype == 1:
        game = GamePlay1x1()
        game.Start()

    elif gametype == 2:

        game = GamePlayWithBot()
        game.Start()



if __name__ == "__main__":
    main()