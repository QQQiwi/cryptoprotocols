import math
import random
import hashlib


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


def generate_prime(length):
    while True:
        p = random.randrange(10 ** (length - 1), 10 ** length)
        if p % 2 == 0:
            p += 1
        if miller_rabin(p, 20):
            return p


def generate_keys():
    print("Введите длину p:")
    p_len = int(input())
    p = generate_prime(p_len)
    print("Введите длину q:")
    q_len = int(input())
    q = generate_prime(q_len)
    
    print("Введите k:")
    k = int(input())

    n = p * q

    ck_list = []
    v_list = []
    for _ in range(k):
        close_key = random.randrange(1, n - 1)
        while math.gcd(close_key, n) != 1:
            close_key = random.randrange(1, n - 1)
        ck_list.append(close_key)
        v = power(close_key, 2, n)
        v_list.append(v)
    
    open_key = v_list, n
        
    with open('open_key.txt', 'w') as file:
        file.write(str(open_key))

    with open('close_key.txt', 'w') as file:
        file.write(str(ck_list))


def calculate_hash(file_path, hash_type="sha256"):
    with open(file_path, 'rb') as file:
        hash_object = hashlib.new(hash_type)
        while chunk := file.read(8192):
            hash_object.update(chunk)
        return hash_object.hexdigest()


def get_message_hash():
    file_name = input()
    file_hash = calculate_hash(file_name)
    inted_hash = ''.join(format(ord(i), '08b') for i in file_hash)
    inted_hash = int(inted_hash, 2)
    return inted_hash


def list_to_matrix(some_list, k):
    mat = []
    while some_list != []:
        mat.append(some_list[:k])
        some_list = some_list[k:]
    return mat


def sign_message():
    open_key = ""
    close_key = ""
    with open('open_key.txt', 'r') as file:
        open_key = file.read()
    with open('close_key.txt', 'r') as file:
        close_key = file.read()
    
    v, n = eval(open_key)
    close_key = eval(close_key)

    print("Введите имя файла, который хотите подписать:")
    message_hash = get_message_hash()
    
    print("Введите t:")
    t = int(input())

    r_list = []
    x_list = []
    for i in range(t):
        r = random.randrange(1, n - 1)
        r_list.append(r)
        x = power(r, 2, n)
        x_list.append(x)

    x = x_list[0]
    for i in range(1, t):
        x = x | x_list[i]

    number_bytes = str(message_hash | x).encode('utf-8')
    hash_object = hashlib.new("sha256")
    hash_object.update(number_bytes)
    h = hash_object.hexdigest()
    string_h = ''.join(format(ord(i), '08b') for i in h)

    bs = []
    k = len(v)
    for i in range(k * t):
        bs.append(int(string_h[i]))
    bs_matrix = list_to_matrix(bs, k)

    y_list = []
    for i in range(t):
        y = r_list[i]
        if bs_matrix[i][0] and 0:
            y = (y * close_key[0]) % n
        y_list.append(y)
    

    with open('sign.txt', 'w') as file:
        file.write(str((bs_matrix, y_list)))


def proof():
    open_key = ""
    sign = ""
    with open('open_key.txt', 'r') as file:
        open_key = file.read()
    with open('sign.txt', 'r') as file:
        sign = file.read()

    v, n = eval(open_key)
    bits, y = eval(sign)

    print("Введите имя файла, подпись которого хотите проверить:")
    message_hash = get_message_hash()

    k = len(v)
    t = len(y)

    z_list = []
    for i in range(t):
        z = pow(y[i], 2, n)
        if bits[i][0] and 0:
            z = (z * v[0]) % n
        z_list.append(z)

    z = z_list[0]
    for i in range(1, t):
        z = z | z_list[i]

    number_bytes = str(message_hash | z).encode('utf-8')
    hash_object = hashlib.new("sha256")
    hash_object.update(number_bytes)
    h = hash_object.hexdigest()
    string_h = ''.join(format(ord(i), '08b') for i in h)

    bs = []
    for i in range(k * t):
        bs.append(int(string_h[i]))
    bs_matrix = list_to_matrix(bs, k)

    if bs_matrix == bits:
        print("Подпись принята.")
    else:
        print("Подпись не принята.")


def main():
    print("Выберите опцию.")
    print("1. Сгенерировать ключи")
    print("2. Подписать сообщение")
    print("3. Проверка подписи")
    option = int(input())
    if option == 1:
        generate_keys()
    elif option == 2:
        sign_message()
    elif option == 3:
        proof()


if __name__ == "__main__":
    main()