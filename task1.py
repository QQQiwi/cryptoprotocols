import math
import random


def power(x, y, mod) :
    if (y == 0) :
        return 1
    temp = power(x, y // 2, mod) % mod
    temp = (temp * temp) % mod
    if (y % 2 == 1) :
        temp = (temp * x) % mod
    return temp


def miller_rabin(n, k):
    if 2 <= n <= 3:
        return True
    if n < 2 or not(n % 2):
        return False
    
    t = n - 1
    s = 0
    while not(t % 2):
        t /= 2
        s += 1
    
    for i in range(k):
        a = random.randint(2, n - 2)
        x = power(a, t, n)
        if x == 1 or x == n - 1:
            continue
        for j in range(s - 1):
            x = (x * x) % n
            if x == 1:
                return False
            if x == n - 1:
                break

        if x != n - 1:
            return False
    
    return True


def alice_r_choose(n):
    print("Пусть Алиса выберет число r (где 1 <= r <= n - 1):")
    r = int(input())
    while not (1 <= r <= n - 1):
        r = int(input())
    
    x = power(r, 2, n)
    return x, r


def bob_e_choose():
    print("Пусть B выберет бит (0 или 1):")
    e = int(input())
    while e not in [0, 1]:
        print("Введите 0 или 1:")
        e = int(input())
    return e


def alice_y_evaluation(r, s, e, n):
    if e:
        y = (r * s) % n
    else:
        y = r
    return y


def bob_proof_approval(y, x, v, e, n):
    if y == 0:
        print("B отвергает доказательство.")
        return False
    else:
        print("Проверка y^2 = x * v^e (mod n).")
        powered_y = power(y, 2, n)
        print(f"y^2 = {powered_y}")
        right_equation_part = (x * power(v, e, n)) % n
        print(f"x * v^e (mod n) = {x} * {v}^{e} (mod {n}) = {right_equation_part}")
        if powered_y == right_equation_part:
            return True


def round_of_proof(s, v, n):
    x, r = alice_r_choose(n)
    e = bob_e_choose()
    y = alice_y_evaluation(r, s, e, n)
    return bob_proof_approval(y, x, v, e, n)


def main():
    print("Доверенный центр T:")
    print("Введите простое число p:")
    p = int(input())
    while not miller_rabin(p, 20):
        print("Число p должно быть простым! Введите p:")
        p = int(input())

    print("Введите простое число q:")
    q = int(input())
    while not miller_rabin(p, 20):
        print("Число q должно быть простым! Введите q:")
        q = int(input())
    
    n = p * q
    print(f"n = {n}.")

    print("Пусть Алиса выберет число s, взаимно-простое с n (где 1 <= s <= n - 1):")
    s = int(input())
    while math.gcd(s, n) != 1 and not (1 <= s <= n - 1):
        print("Число s должно быть взаимно-простым с n! Введите s:")
        s = int(input())

    v = power(s, 2, n)
    print(f"V равен {s}^2 (mod {n}) = {v}.")

    print("Введите число раундов t, после которых Боб посчитает знание доказанным:")
    t = int(input())

    for i in range(t):
        print(f"Раунд {i + 1}:")
        if not round_of_proof(s, v, n):
            return 0
        print(f"Раунд {i + 1} завершен.")
    
    print(f"Все {t} раундов прошли успешно.")
    return 0
    

if __name__ == "__main__":
    main()