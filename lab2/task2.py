import math
import random
import copy


def get_adj_list_by_matrix(matrix):
    n = len(matrix)
    adj_list = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(n):
            if i != j and matrix[i][j]:
                if j not in adj_list[i]:
                    adj_list[i].append(j)
                if i not in adj_list[j]:
                    adj_list[j].append(i)
    return adj_list


def get_adj_matrix_by_list(adj_list):
    n = len(adj_list.keys())
    new_graph = [[0 for _ in range(n)] for _ in range(n)]
    for k in adj_list.keys():
        for i in adj_list[k]:
            new_graph[k][i] = 1
            new_graph[i][k] = 1
    return new_graph


def generate_isomorphism(n, save=True):
    # с помощью циклической перестановки
    permutation = list(range(n))
    while True:
        is_good = True
        random.shuffle(permutation)
        permutation = [permutation[-1]] + permutation[:-1]    
        for i in range(len(permutation)):
            if permutation[i] == i:
                is_good = False
                break
        if is_good == True:
            break

    isomorphism = {i: permutation[i] for i in range(n)}

    if save:
        with open('isomorphism.txt', 'w') as file:
            file.write(str(isomorphism))

    return isomorphism


def apply_isomorphism(graph=None, iso=None, from_file=True):
    if graph is None:
        with open('graph.txt', 'r') as file:
            graph = file.read()
        graph = eval(graph)

    if from_file:
        with open('isomorphism.txt', 'r') as file:
            iso = file.read()
        iso = eval(iso)

    n = len(graph)
    # adj_list = get_adj_list_by_matrix(graph)
    adj_list = graph
    new_adj_list = {iso[i]: [iso[j] for j in adj_list[i]] for i in range(n)}
    # new_graph = get_adj_matrix_by_list(new_adj_list)
    new_graph = new_adj_list
    return new_graph


def generate_graph(n, k, by_iso=False, save=True):
    if by_iso:
        new_graph = apply_isomorphism()
        with open('graph2.txt', 'w') as file:
            file.write(str(sort_dict_n_lists(new_graph)))
        return new_graph
    
    if n <= 0:
        raise ValueError("Число вершин должно быть положительным.")

    if k % 2 != 0:
        raise ValueError("k должно быть четным для графа с нечетным числом вершин.")

    # Создаем пустой граф с n вершинами
    graph = [[0 for _ in range(n)] for _ in range(n)]

    # Генерируем случайные ребра
    for i in range(n):
        for j in range(1, k // 2 + 1):
                graph[i][(i + j) % n] = 1
                graph[(i + j) % n][i] = 1

    graph = get_adj_list_by_matrix(graph)

    if save:
        with open('graph.txt', 'w') as file:
            file.write(str(sort_dict_n_lists(graph)))
    return graph


def zero_step():
    print("Введите число вершин в графе:")
    n = int(input())
    print("Введите величину степени вершин в графе:")
    p = int(input())

    generate_graph(n, p)
    print("Первый граф сгенерирован и сохранен в graph.txt")

    iso = generate_isomorphism(n)
    print("Изоморфизм сохранен в isomorphism.txt")

    generate_graph(n, p, by_iso=True)
    print("Второй граф сгенерирован и сохранен в graph2.txt")


def first_step():
    with open('graph.txt', 'r') as file:
        graph = file.read()
    graph = eval(graph)
    n = len(graph)

    iso_G1_to_H = generate_isomorphism(n, save=False)
    with open('isomorphism_G1_to_H.txt', 'w') as file:
        file.write(str(iso_G1_to_H))
    
    with open('isomorphism.txt', 'r') as file:
        iso_G1_to_G2 = file.read()
    iso_G1_to_G2 = eval(iso_G1_to_G2)

    iso_G2_to_G1 = {v: k for k, v in iso_G1_to_G2.items()}
    iso_G2_to_H = {i: iso_G1_to_H[iso_G2_to_G1[i]] for i in range(n)}
    with open('isomorphism_G2_to_H.txt', 'w') as file:
        file.write(str(iso_G2_to_H))

    graph_H = apply_isomorphism(iso=iso_G1_to_H, from_file=False)
    with open('graph_H.txt', 'w') as file:
        file.write(str(sort_dict_n_lists(graph_H)))


def sort_dict_n_lists(some_dict):
    some_dict_keys = list(some_dict.keys())
    some_dict_keys.sort()
    for i in some_dict_keys:
        some_dict[i].sort()
    some_dict = {i: some_dict[i] for i in some_dict_keys}
    return some_dict


def compare_two_dicts(dict1, dict2):
    common_keys = set(dict1.keys()) & set(dict2.keys())
    for key in common_keys:
        if dict1[key] != dict2[key]:
            return False
    return True


def proof():
    print("Выберите:")
    print("1 - Доказать, что G_1 и H изоморфны.")
    print("2 - Доказать, что G_2 и H изоморфны.")
    n = int(input())
    
    iso = {}
    graph = None
    if n == 1:
        with open('graph.txt', 'r') as file:
            graph = file.read()
        graph = eval(graph)

        with open('isomorphism_G1_to_H.txt', 'r') as file:
            iso_G1_to_H = file.read()
        iso = eval(iso_G1_to_H)
    if n == 2:
        with open('graph2.txt', 'r') as file:
            graph = file.read()
        graph = eval(graph)

        with open('isomorphism_G2_to_H.txt', 'r') as file:
            iso_G2_to_H = file.read()
        iso = eval(iso_G2_to_H)
    
    with open('graph_H.txt', 'r') as file:
        graph_H = file.read()
    graph_H = eval(graph_H)
    graph_H = sort_dict_n_lists(graph_H)

    iso_graph_H = sort_dict_n_lists(apply_isomorphism(graph, iso, False))
    if not compare_two_dicts(graph_H, iso_graph_H):
        print("Графы не изоморфны!")
    else:
        print("Графы изоморфны!")
        print(f"G{n} -> H")
        for k, v in iso.items():
            print(f"{k} -> {v}")


def main():
    print("Выберите опцию:")
    print("0 - Сгенерировать графы G_1, G_2 и изоморфизм.")
    print("1 - Перетасовать граф G_1 и получить новый граф H.")
    print("2 - Доказательство изоморфности.")
    n = int(input())
    if n == 0:
        zero_step()
    if n == 1:
        try:
            first_step()
        except:
            print("Нарушение целостности файлов!")
    if n == 2:
        proof()


if __name__ == "__main__":
    main()