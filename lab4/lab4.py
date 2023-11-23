# Протокол Диффи – Хельмана.
import math
import random
import hashlib
from Crypto.Util.number import getPrime
from functools import reduce


def factors(n, q):    
    nums = set()
    nums.add(q)
    while n != 1:
        for i in range(2, n + 1):
            if n % i == 0:
                nums.add(i)
                n //= i
                break
    return nums


def power(x, y, mod) :
    if (y == 0) :
        return 1
    temp = power(x, y // 2, mod) % mod
    temp = (temp * temp) % mod
    if (y % 2 == 1) :
        temp = (temp * x) % mod
    return temp


def gcd(a,b):
    while b != 0:
        a, b = b, a % b
    return a


def find_g_value(p, q):
    nums = [q, 2]
    for g in range(2, p):
        fl = True
        for el in nums:
            if pow(g, el, p) == 1:
                fl = False
                break
        if fl:
            return g
    return -1


def miller_rabin(n, k):
    if 2 <= n <= 3:
        return True
    if n < 2 or not(n % 2):
        return False
    
    t = n - 1
    s = 0
    while not(t % 2):
        t = t // 2
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


def generate_number(length):    
    p = 1 << (length - 1)
    for _ in range(length - 1):
        random_bit = random.randint(0, 1)
        p = (p << 1) | random_bit
    return p


def prime_numbers_generation(l):
    q = getPrime(l)
    t = 1
    pM1 = 2**t * q
    while not miller_rabin(pM1 + 1, 2):
        t += 1
        pM1 = 2 ** t * q
    return pM1 + 1, q, t


def generate_public_key():
    print("Введите длину p:")
    p_len = int(input())
    p, q, t = prime_numbers_generation(p_len)
    g = find_g_value(p, q)
    
    with open('public_key.txt', 'w') as file:
        file.write(str((g, p)))


def generate_private_keys(n):
    with open('public_key.txt', 'r') as file:
        pk = file.read()
    g, p = eval(pk)
    
    a_power = random.randint(1, p)
    b_power = random.randint(1, p)

    if n == 2:
        with open('alice_private_key.txt', 'w') as file:
            file.write(str(a_power))

    if n == 3:
        with open('bob_private_key.txt', 'w') as file:
            file.write(str(b_power))

    if n == 4:
        with open('alice_private_key.txt', 'r') as file:
            apk = file.read()
        a_power = eval(apk)
        a = pow(g, a_power, p)
        with open('alice_remainder.txt', 'w') as file:
            file.write(str(a))

    if n == 5:
        with open('bob_private_key.txt', 'r') as file:
            apk = file.read()
        b_power = eval(apk)
        b = pow(g, b_power, p)
        with open('bob_remainder.txt', 'w') as file:
            file.write(str(b))
    


def calculate_k():
    with open('public_key.txt', 'r') as file:
        pk = file.read()
    g, p = eval(pk)

    with open('alice_private_key.txt', 'r') as file:
        apk = file.read()
    a = eval(apk)

    with open('bob_private_key.txt', 'r') as file:
        bpk = file.read()
    b = eval(bpk)

    with open('alice_power.txt', 'r') as file:
        ap = file.read()
    a_power = eval(ap)

    with open('bob_power.txt', 'r') as file:
        bp = file.read()
    b_power = eval(bp)

    alice_K = pow(b, a_power, p)
    bob_K = pow(a, b_power, p)

    if alice_K == bob_K:
        print("Вычисленные значения совпадают!")


def calculate_k_alice():
    with open('public_key.txt', 'r') as file:
        pk = file.read()
    _, p = eval(pk)

    with open('bob_remainder.txt', 'r') as file:
        bpk = file.read()
    b = eval(bpk)

    with open('alice_private_key.txt', 'r') as file:
        ap = file.read()
    a_power = eval(ap)

    alice_K = pow(b, a_power, p)

    print("Вычисленное Алисой значение K: ", alice_K)


def calculate_k_bob():
    with open('public_key.txt', 'r') as file:
        pk = file.read()
    _, p = eval(pk)

    with open('alice_remainder.txt', 'r') as file:
        apk = file.read()
    a = eval(apk)

    with open('bob_private_key.txt', 'r') as file:
        bp = file.read()
    b_power = eval(bp)

    bob_K = pow(a, b_power, p)
    
    print("Вычисленное Бобом значение K: ", bob_K)


def main():
    print("Выберите действие:")
    print("1 - Сгенерировать g и p (публичный ключ).")
    print("2 - Сгенерировать a.")
    print("3 - Сгенерировать b.")
    print("4 - Сгенерировать A = g^a mod p.")
    print("5 - Сгенерировать B = g^b mod p.")
    print("6 - Вычислить K для Алисы.")
    print("7 - Вычислить K для Боба.")

    n = int(input())
    if n == 1:
        generate_public_key()
    elif n in [2, 3, 4, 5]:
        generate_private_keys(n)
    elif n == 6:
        calculate_k_alice()
    elif n == 7:
        calculate_k_bob()


if __name__ == "__main__":
    main()