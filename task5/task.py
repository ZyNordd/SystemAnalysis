import json
import numpy as np

def parse_ranking(ranking):
    """
    Преобразует ранжировку в словарь, где каждому элементу сопоставляется индекс его уровня.
    """
    rankings = {}
    for level, group in enumerate(ranking):
        if isinstance(group, list):
            for item in group:
                rankings[item] = level
        else:
            rankings[group] = level
    return rankings

def calculate_matrix(ranking):
    """
    Строит матрицу согласования на основе ранжировки.
    """
    rankings = parse_ranking(ranking)
    num_elements = len(rankings)
    matrix = []

    for i in range(1, num_elements + 1):
        row = []
        for j in range(1, num_elements + 1):
            row.append(1 if rankings[j] >= rankings[i] else 0)
        matrix.append(row)

    return matrix

def find_core_conflicts(matrix_a, matrix_b):
    """
    Определяет ядро противоречий между двумя матрицами согласования.
    """
    matrix_a, matrix_b = np.array(matrix_a), np.array(matrix_b)
    product_direct = matrix_a * matrix_b
    product_transposed = matrix_a.T * matrix_b.T
    conflict_matrix = np.logical_or(product_direct, product_transposed)
    
    # Ищем пары, где нет согласования
    conflicts = []
    for i in range(len(conflict_matrix)):
        for j in range(i + 1, len(conflict_matrix)):
            if not conflict_matrix[i, j] and not conflict_matrix[j, i]:
                conflicts.append([i + 1, j + 1])
    return conflicts

def main(json_a, json_b):
    """
    Основная функция, которая получает две ранжировки в формате JSON строки,
    вычисляет ядро противоречий и возвращает результат в формате JSON строки.
    Для наглядности в консоль выведено ядро противоречий в формате JSON.
    """

    # Преобразование JSON-строк в объекты Python
    ranking_a = json.loads(json_a)
    ranking_b = json.loads(json_b)

    # Вычисление матриц согласования
    matrix_a = calculate_matrix(ranking_a)
    matrix_b = calculate_matrix(ranking_b)

    # Определение ядра противоречий
    conflicts = find_core_conflicts(matrix_a, matrix_b)

    # Формирование результата в формате JSON
    result = conflicts
    print(json.dumps(result, indent=4))
    return result

#Тестовые данные
a = '[1, [2, 3], 4, [5, 6, 7], 8, 9, 10]'
b = '[[1, 2], [3, 4, 5], 6, 7, 9, [8, 10]]'

# Запуск программы
if __name__ == "__main__":
    main(a, b)
