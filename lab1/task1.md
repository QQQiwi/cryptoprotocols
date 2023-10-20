Задание выполнил Улитин Иван Владимирович, 531 группа

# Краткая теория

Выбирается $n$ - произведение двух больших простых чисел. Генерируется открытый ключ $v_1, v_2, \dots, v_k$ и закрытый ключ $s_1, s_2, \dots, s_k$, где $v_i = s_i^2 \pmod n$ (и $s_i$ взаимно-простое с $n$).

1. Алиса выбирает $t$ случайных целых чисел в диапазоне $[1, n - 1]$: $r_1, r_2, \dots, r_t$ - и вычисляет $x_1, x_2, \dots, x_t$, такие что $x_i = r_i^2 \pmod n$.

2. Алиса хэширует объединение сообщения и строки $x_i$, создавая битовый поток: $H(m, x_1, \dots, x_t)$. Она использует первые $k \cdot t$ битов этой строки в качестве значений $b_{ij}$, где $i$ пробегает от $1$ до $t$, а $j$ от $1$ до $k$.

3. Алиса вычисляет $y_1, y_2, \dots, y_t$, где $y_i = r_i \cdot (s_1^{b_{i1}} \cdot s_2^{b_{i2}} \cdots s_k^{b_{ik}}) \pmod n$

4. Алиса посылает Бобу $m$, все биты $b_{ij}, все значения $y_i$. У Боба уже
   есть открытый ключ Алисы: $v_1, v_2, \dots, v_k$.

5. Боб вычисляет $z_1, z_2, \dots, z_t$, где $z_i = y_i^2 \cdot (v_1^{b_{i1}} \cdot v_2^{b_{i2}} \cdots v_k^{b_{ik}}) \pmod n$

6. Боб проверяет, что первые $k \cdot t$ битов $H(m, z_1, \dots, z_t)$ - это значения $b_{ij}$, которые прислала ему Алиса.

Как и в схеме идентификации безопасность схемы подписи пропорциональна $1/2^{kt}$.

## Особенности программной реализации

При запуске программы предлагается выбрать одну из опций: сгенерировать ключи, подписать сообщение, проверка подписи.

1. При выборе опции "сгенерировать ключи" нужно ввести длину $p$, $q$ и число $k$. В качестве выхода программы в данном случае будут файлы ```close_key.txt``` и ```open_key.txt``` - файлы, содержащие закрытый и открытый ключом соответственно. Они будут использованы для двух других опций.

2. При выборе "подписать сообщение" необходимо ввести имя файла, которое требуется подписать, и ввести число $t$. Результатом работы программы будет файл подписи ```sign.txt```.

3. При выборе "проверка подписи" необходимо ввести имя проверяемого файла. Если проверка подписи будет пройдена, программа выведет в консоль надписть "Подпись принята.", иначе "Подпись не принята."

## Доказательство

Доказательство следует напрямую из работы Фиата и Шамира, которое там приведено в качестве леммы:

Если Алиса и Боб следуют протоколу, то Боб всегда будет принимать проверку
подписи корректной.

$$y_i^2 \prod_{b_{ij} = 1} v_j = r_i^2 \prod_{b_{ij} = 1} (s^2_j v_j) = r_i^2 = x_i \pmod n$$