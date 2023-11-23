from secrets import randbits
import random
from random import randint
from hashlib import sha1


def write_list_hash(name, lst, filename='alice-list.txt', fl=True):
    try:
        if fl:
            f = open(filename, 'a+')
        else:
            f = open(filename, 'w+')
        
        for i in range(len(lst) - 1, -1, -1):
            f.writelines(f'{lst[i]}\n')
        f.close()
    except:
        print('\nОшибка записи.\n')


def generate_new_nums(r, t):
    tmp = sha1(str(r).encode("utf-8"))
    hashes = [tmp.hexdigest()]
    for i in range(1, t + 1):
        tmp = sha1(str(hashes[i - 1]).encode("utf-8"))
        hashes.append(tmp.hexdigest())
    return hashes


def delete_old_values_from_file(name, filename='host-list.txt'):
    try:
        f = open(filename, 'r')
        data = f.read().split('\n')
        f.close()
    except:
        return
    else:
        new_data = []
        for el in data:
            if el != '' and name not in el:
                new_data.append(el)
        g = open(filename, 'w+')
        for i in range(len(new_data)):
            g.write(f'{new_data[i]}\n')
        g.close()


def generate_hash():
    name = "alice"
    with open('r.txt', 'r') as file:
        r = file.read()
    r = eval(r)
    t = int(input("Введите количество вычисляемых значений с помощью"
                  " хеш-функции t:\n"))
    hashes = generate_new_nums(r, t)
    delete_old_values_from_file(name)
    write_list_hash(name, hashes, 'host-list.txt')
    write_list_hash(name, hashes[:-1], f'{name}-list.txt', False)


def gcd(a,b):
    while b != 0:
        a, b = b, a % b
    return a


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
    
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, t, n)
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


def generate_l_bit(l):
    num = int(randbits(l))
    while (num < 2):
        num = int(randbits(l))
    return num


def prime_numbers_generation(l):
    q = generate_l_bit(l)
    while not miller_rabin(q, 10):
        q = generate_l_bit(l)
    return q


def write_values(r, filename):
    f = open(filename, 'w')
    f.write(f'{r}')
    f.close()


def read_list(name, filename):
    def data_format(name, data):
        new_data = []
        for el in data:
            if el != '':
                new_data.append(el[el.find(':') + 1:])
        return new_data
    try:
        f = open(filename, 'r')
        data = f.read().split('\n')
    except:
        print('\nОшибка считывания данных с файла')
        return []
    
    return data, data_format(name, data)


def write_list(lst, filename='alice-list.txt'):
    try:
        f = open(filename, 'w+')
        for i in range(len(lst)):
            f.write(f'{lst[i]}\n')
        f.close()
    except:
        print('\nОшибка записи данных в файл!!!\n')
    else:
        print(f'Новые данные были записаны в файл {filename}')


def compare(x, verific_val):
    t = sha1(x.encode("utf-8"))
    if t.hexdigest() == verific_val:
        return True
    return False



def authentication():
    name = "alice"
    passwd = input('Введите значение x: ')
    filename = 'host-list.txt'
    common_data, data = read_list(name, filename)
    if len(data) == 1:
        print('\nЗначения для подтверждения аутентификации закончились.'
              '\nНужно сгенерировать x.\n')
        return

    if compare(passwd, data[0]):
        print(f'\nАлиса успешно прошла аутентификацию\n')
        new_data = []
        for el in common_data:
            if data[0] not in el:
                new_data.append(el)
        write_list(new_data, filename)
    else:
        print(f'\nОшибка. Алиса не прошла аутентификацию\n')


def generate_r():
    l = int(input("Введите значение l (количество бит числа q):\n"))
    try:
        r = generate_l_bit(l)
        f = open('r.txt', 'w')
        f.write(f'{r}')
        f.close()
        print("Случайное число R сгенерировано.")
    except:
        print("Возникла ошибка.")


def main():
    print("Выберите опцию:")
    print("1 - Сгенерировать R")
    print("2 - Сгенерировать значения x с помощью хэш-функций")
    print("3 - Провести аутентификацию Алисы")
    option = int(input())
    if option == 1:
        generate_r()
    elif option == 2:
        generate_hash()
    elif option == 3:
        authentication()


if __name__ == "__main__":
    main()