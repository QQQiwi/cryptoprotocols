
import random
import string
from Crypto.Util.number import getPrime
import os
import shutil
from os.path import isfile, join


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


cur_dir = "cards"
cards_list = [
    "Двойка Буби", "Двойка Крести", "Двойка Черви", "Двойка Пики",
    "Тройка Буби", "Тройка Крести", "Тройка Черви", "Тройка Пики",
    "Четверка Буби", "Четверка Крести", "Четверка Черви", "Четверка Пики",
    "Пятерка Буби", "Пятерка Крести", "Пятерка Черви", "Пятерка Пики",
    "Шестерка Буби", "Шестерка Крести", "Шестерка Черви", "Шестерка Пики",
    "Семерка Буби", "Семерка Крести", "Семерка Черви", "Семерка Пики",
    "Восьмерка Буби", "Восьмерка Крести", "Восьмерка Черви", "Восьмерка Пики",
    "Девятка Буби", "Девятка Крести", "Девятка Черви", "Девятка Пики",
    "Десятка Буби", "Десятка Крести", "Десятка Черви", "Десятка Пики",
    "Валет Буби", "Валет Крести", "Валет Черви", "Валет Пики",
    "Дама Буби", "Дама Крести", "Дама Черви", "Дама Пики",
    "Король Буби", "Король Крести", "Король Черви", "Король Пики",
    "Туз Буби", "Туз Крести", "Туз Черви", "Туз Пики",
        ]


def generate_keys(prime_number):
    while True:
        x = random.randint(1, prime_number - 1)
        while gcd(x, prime_number) != 1:
            x = random.randint(1, prime_number - 1)
        for y in range(2, prime_number):
            if (x * y) % (prime_number - 1) == 1:
                return x, y


def encrypt(mes, x, mod, first=True):
    if not first:
        mes_list = list(eval(mes))
        mes_list = [pow(number, x, mod) for number in mes_list]
        mes_str = "".join(str(mes_elem) + "," for mes_elem in mes_list)
        return mes_str[:-1]
    else:
        encrypted_message = "".join(str(pow(ord(let), x, mod)) + "," for let in mes)
        return encrypted_message[:-1]
            


def decrypt(emes, y, mod, last=False):
    if last:
        emessage_list = emes.split(",")
        message = "".join(chr(pow(int(let), y, mod)) for let in emessage_list)
        return message
    else:
        emes_list = emes.split(",")
        mes_list = [pow(int(number), y, mod) for number in emes_list]
        mes = "".join(str(number) + "," for number in mes_list)
        return mes[:-1]


def reshuffle():
    bob_card_list = []
    onlyfiles = [f for f in os.listdir(cur_dir) if isfile(join(cur_dir, f))]
    for one_file in onlyfiles:
        file_content = ""
        with open(f"{cur_dir}/{one_file}", 'r') as file:
            file_content = file.read()
        bob_card_list.append(file_content)
    random.shuffle(bob_card_list)
    shutil.rmtree(cur_dir)
    os.mkdir(cur_dir)
    for card_i in range(len(bob_card_list)):
        with open(f'{cur_dir}/{card_i}.txt', 'w', encoding='utf-8') as file:
            file.write(bob_card_list[card_i])


def get_player_number(player_name, player_dict):
    for number, pl_name in player_dict.items():
        if player_name == pl_name:
            return number


def distribute():
    print("Введите имя игрока, которому хотите раздать/досдать карты:")
    player_name = input()
    print("Введите число карт, которое хотите раздать/досдать:")
    card_amount = int(input())
    cardfiles = [f for f in os.listdir(cur_dir) if isfile(join(cur_dir, f))]
    if len(cardfiles) < card_amount:
        print("Карт в колоде меньше, чем введенное значение!")
        return None
    player_card_list = cardfiles[:card_amount]
    try:
        os.mkdir(player_name)
    except:
        pass
    
    with open(f"keys_{player_name}.txt", 'r') as file:
        keys = file.read()
        keys = eval(keys)
    x, _, p = keys

    for card in player_card_list:
        card_content = ""
        with open(f"{cur_dir}/{card}", 'r') as file:
            card_content = file.read()
        os.remove(f"{cur_dir}/{card}")
        keys = ""
        enc_card_content = encrypt(card_content, x, p, False)
        with open(f'{player_name}/{card}', 'w', encoding='utf-8') as file:
            file.write(enc_card_content)


def decrypt_by_diller():
    print("Введите имя игрока, карты которого хотите расшифровать ключом диллера:")
    player_name = input()
    print("Введите имя диллера:")
    diller_name = input()
    with open(f"keys_{diller_name}.txt", 'r') as file:
        keys = file.read()
        keys = eval(keys)
    _, y, p = keys

    decrypt_dir = "decrypt_" + player_name
    os.mkdir(decrypt_dir)
    cardfiles = [f for f in os.listdir(player_name) if isfile(join(player_name, f))]
    
    for card in cardfiles:
        card_content = ""
        with open(f"{player_name}/{card}", 'r') as file:
            card_content = file.read()
        keys = ""
        d_card_content = decrypt(card_content, y, p)
        with open(f'{decrypt_dir}/{card}', 'w', encoding='utf-8') as file:
            file.write(d_card_content)


def decrypt_by_player():
    print("Введите имя игрока, карты которого хотите расшифровать окончательно.")
    player_name = input()
    with open(f"keys_{player_name}.txt", 'r') as file:
        keys = file.read()
        keys = eval(keys)
    _, y, p = keys

    decrypt_dir = "decrypt_" + player_name
    final_dir = "final_" + decrypt_dir
    os.mkdir(final_dir)
    cardfiles = [f for f in os.listdir(decrypt_dir) if isfile(join(decrypt_dir, f))]

    for card in cardfiles:
        card_content = ""
        with open(f"{decrypt_dir}/{card}", 'r') as file:
            card_content = file.read()
        keys = ""
        d_card_content = decrypt(card_content, y, p, True)
        with open(f'{final_dir}/{card}', 'w', encoding='utf-8') as file:
            file.write(d_card_content)


def decrypt_diller():
    print("Введите имя диллера:")
    diller_name = input()
    with open(f"keys_{diller_name}.txt", 'r') as file:
        keys = file.read()
        keys = eval(keys)
    _, y, p = keys
    
    decrypt_dir = "decrypt_" + cur_dir
    os.mkdir(decrypt_dir)
    cardfiles = [f for f in os.listdir(cur_dir) if isfile(join(cur_dir, f))]
    
    for card in cardfiles:
        card_content = ""
        with open(f"{cur_dir}/{card}", 'r') as file:
            card_content = file.read()
        keys = ""
        d_card_content = decrypt(card_content, y, p, True)
        with open(f'{decrypt_dir}/{card}', 'w', encoding='utf-8') as file:
            file.write(d_card_content)


def generate_player_n_keys():
    print("Введите длину простого числа в битах (общий модуль):")
    p_len = int(input())
    p = getPrime(p_len)
    print("Сгенерировано простое число:", p)
    print("Введите количество игроков:")
    player_amount = int(input())
    
    for i in range(player_amount):
        print(f"Введите имя {i + 1}-го игрока:")
        player_i = input()
        x, y = generate_keys(p)
        with open(f'keys_{player_i}.txt', 'w') as file:
            file.write(str((x, y, p)))
        print(f"Ключи для {player_i} сгенерированы и сохранены")


def create_deck():
    print("Введите имя диллера:")
    diller_name = input()
    keys = ""
    with open(f"keys_{diller_name}.txt", 'r') as file:
        keys = file.read()
        keys = eval(keys)
    x, _, p = keys
    
    files_list = []
    try:
        os.mkdir(cur_dir)
    except:
        shutil.rmtree(cur_dir)
        os.mkdir(cur_dir)
    random.shuffle(cards_list)
    for card_i in range(len(cards_list)):
        card = cards_list[card_i]
        card_content = card + ", " + str(random.randint(1, p))
        enc_card_content = encrypt(card_content, x, p)
        with open(f'{cur_dir}/{card_i}.txt', 'w', encoding='utf-8') as file:
            file.write(enc_card_content)
        files_list.append((card_i, card_content))
    with open(f'diller_memory.txt', 'w', encoding='utf-8') as file:
        file.write(str(files_list))


if __name__ == "__main__":
    print("Выберите действие:")
    print("1 - Сгенерировать список игроков и ключи для них")
    print("2 - Создать колоду с помощью диллера")
    print("3 - Перетасовать колоду")
    print("4 - Расдача/досдача карт игрокам")
    print("5 - Расшифровать диллером для игрока")
    print("6 - Расшифровать игроком")
    print("7 - Расшифровать диллеру (все оставшиеся карты)")
    move = int(input())
    if move == 1:
        generate_player_n_keys()
    if move == 2:
        create_deck()
    if move == 3:
        reshuffle()
    if move == 4:
        distribute()
    if move == 5:
        decrypt_by_diller()
    if move == 6:
        decrypt_by_player()
    if move == 7:
        decrypt_diller()
