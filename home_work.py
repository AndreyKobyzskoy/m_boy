import random as rd

kp = 6
kv = 4
kk = 7


class Doska:
    def __init__(self):
        self.fild = [['0' for j in range(kp)] for i in range(kp)]
        self.fild1 = [['0' for j in range(kp)] for i in range(kp)]
        self.mzk = set(())
        self.mzk1 = set(())
        self.skrb = {0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: None}

    def out(self):

        print(' ' * 5, 'Моё поле', ' ' * 25, 'Поле противника')
        print(' ' * 3, '1 2 3 4 5 6', ' ' * 22, ' ' * 3, '1 2 3 4 5 6')
        for i in range(kp):
            print(' ', (i + 1), end='')
            for j in range(kp):
                print('|', self.fild[i][j], '', sep='', end='')
            print('|', end='')
            print(' ' * 24, (i + 1), end='')
            for j in range(kp):
                print('|', self.fild1[i][j], '', sep='', end='')
            print('|')
        print()

    def set_kr(self):

        for i in range(kk):

            if i == 0:
                x = rd.randint(0, kp - 1)
                y = rd.randint(0, kp - 1)
                pvr = rd.randint(1, kv)
                x1, y1, pvr = self.psk(x, y, pvr)
                x2, y2 = self.newk(x1, y1, pvr)
                if not self.pr_k(x2, y2, True):
                    x2, y2 = self.newk(x, y, (pvr + 2) % kv)
                self.set_zr([[x, y], [x1, y1], [x2, y2]], self.mzk)
                kr = Korbl([[x, y], [x1, y1], [x2, y2]], self.fild)
                self.skrb[0] = kr

            elif i == 1 or i == 2:
                while True:
                    x = rd.randint(0, kp - 1)
                    y = rd.randint(0, kp - 1)
                    if not self.pr_k(x, y, True):
                        continue
                    pvr = rd.randint(1, kv)
                    x1, y1, pvr = self.psk(x, y, pvr)
                    if pvr != None:
                        break
                self.set_zr([[x, y], [x1, y1]], self.mzk)
                kr = Korbl([[x, y], [x1, y1]], self.fild)
                self.skrb[i] = kr

            elif i > 2:
                while True:
                    x = rd.randint(0, kp - 1)
                    y = rd.randint(0, kp - 1)
                    if self.pr_k(x, y, True):
                        break
                self.set_zr([[x, y]], self.mzk)
                kr = Korbl([[x, y]], self.fild)
                self.skrb[i] = kr

    def newk(self, x, y, pvr):

        if pvr == 1:
            x1 = x;    y1 = y + 1
        elif pvr == 2:
            x1 = x + 1;  y1 = y
        elif pvr == 3:
            x1 = x;    y1 = y - 1
        else:
            x1 = x - 1;  y1 = y
        return x1, y1

    def psk(self, x, y, pvr):

        for i in range(2):
            x1, y1 = self.newk(x, y, pvr)
            if self.pr_k(x1, y1, self.mzk):
                return x1, y1, pvr
            pvr = (pvr + 2) % kv
        return None, None, None

    def pr_k(self, x, y, fl):

        if x < 0 or x >= kp or y < 0 or y >= kp:
            return False
        if fl:
            if (x, y) in self.mzk:
                return False
            else:
                return True
        else:
            if (x, y) in self.mzk1:
                return False
            else:
                return True

    def set_zr(self, krd, mzk):

        for (x, y) in krd:
            mzk.add((x, y))
            mzk.add((x + 1, y))
            mzk.add((x - 1, y))
            mzk.add((x, y + 1))
            mzk.add((x, y - 1))

    def ydar_in(self, x0, y0):

        for krb in self.skrb.values():
            rez = krb.prs(x0, y0, self.fild)
            if rez != 0:
                break
        else:
            self.fild[x0][y0] = '•'
        return rez

    def ydar_out(self, x0, y0, rez):

        if rez == 0:
            self.fild1[x0][y0] = '•'
            self.mzk1.add((x0, y0))
        elif rez == 1:
            self.mzk1.add((x0, y0))
            self.fild1[x0][y0] = 'X'
        else:
            self.set_zr([[x0, y0]], self.mzk1)
            self.fild1[x0][y0] = 'X'


class Korbl:  # Класс кораблей
    def __init__(self, krd, fild):
        self.sst = 0
        self.krd = []
        self.raz = len(krd)
        for [x, y] in krd:
            fild[x][y] = '█'
            self.krd.append([x, y])

    def prs(self, x0, y0, fild):

        for (x, y) in self.krd:
            if x == x0 and y == y0:
                self.sst += 1
                fild[x][y] = 'X'
                if self.sst == self.raz:
                    return 2
                else:
                    return 1
        return 0


class Game():
    def __init__(self):
        self.kv1 = 0
        self.kv2 = 0

    def start(self):
        ds1 = Doska()
        ds2 = Doska()
        print('   Начинаем игру!')
        print("Расставляем на поле игры корабли,\n ваша расстоновка уважаемый!")
        ds1.set_kr()
        ds1.out()
        ds2.set_kr()
        while True:
            # ход юзера
            while True:
                while True:
                    try:
                        x, y = map(int, input('Введи координаты выстрела: ').split())
                    except:
                        print('Не корректный ввод!')
                    x -= 1;
                    y -= 1
                    if not ds1.pr_k(x, y, False):
                        print('Не допустимые значения координат!')
                    else:
                        break
                rez = ds2.ydar_in(x, y)  # проверка результата моего выстрела на доске компа
                ds1.ydar_out(x, y, rez)  # Полученый результат обрабатывается на моей второй доске
                ds1.out()
                if rez == 2:
                    self.kv1 += 1
                    if self.kv1 == kk:
                        print("Потоплен последний корабль противника. Полная победа!\n Конец игры.")
                        return
                    else:
                        print('Вы потопили еще один корабль противника! Продолжайте огонь!')
                elif rez == 1:
                    print('Попадание в корабль противника! Продолжайте огонь!')
                else:
                    print('Мимо! Целься лучше!')
                    break
                # ход компьютера
            while True:
                while True:
                    x = rd.randint(0, kp - 1)
                    y = rd.randint(0, kp - 1)
                    if ds2.pr_k(x, y, False): break
                rez = ds1.ydar_in(x, y)
                ds2.ydar_out(x, y, rez)
                print('Выстрел противника:')
                ds1.out()
                if rez == 2:
                    self.kv2 += 1
                    if self.kv2 == kk:
                        print("Победа противника над тобой!\n Конец игры.")
                        return
                    else:
                        print('Твой корабль потоплен! Противник продолжает огонь!')
                elif rez == 1:
                    print('Попадание в твой корабль! Противник продолжает огонь!')
                else:
                    print('Противник промазал! Твой выстрел!')
                    break


def main():
    gm = Game()
    gm.start()


main()
