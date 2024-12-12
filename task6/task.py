import json

def calculate_mu(x, points):
    """
    Рассчитывает степень принадлежности (μ) для заданного значения x по заданной функции принадлежности.
    """
    for i in range(len(points) - 1):
        x0, mu0 = points[i]
        x1, mu1 = points[i + 1]
        if x0 <= x <= x1:
            return mu0 if mu0 == mu1 else mu0 + (mu1 - mu0) * (x - x0) / (x1 - x0)
    return 0


def fuzz(input_value, fuzzy_set):
    """
    Фаззификация: вычисляет степени принадлежности для входного значения по всем термам.
    """
    mu_vals = {}

    for term, points in fuzzy_set.items():
        mu_vals[term] = round(calculate_mu(input_value, points), 2)

    print(f"Результат фаззификации температуры {input_value}: {mu_vals}\n")
    return mu_vals


def map_to_regulator(temperature_mu_vals, transition_map):
    """
    Проецирует степени принадлежности входных термов на выходные термы по заданным правилам.
    """
    regulator_mu_vals = {}

    for temp_term, temp_mu in temperature_mu_vals.items():
        reg_term = transition_map[temp_term]
        if reg_term in regulator_mu_vals:
            regulator_mu_vals[reg_term] = max(regulator_mu_vals[reg_term], temp_mu)
        else:
            regulator_mu_vals[reg_term] = temp_mu
    
    print(f"Результат проекции на нечеткое множество положений регулятора: {regulator_mu_vals}\n")
    return regulator_mu_vals


def aggregate_outputs(regulator_mu_vals, fuzzy_set):
    """
    Объединяет функции принадлежности выходных термов, обрезая их по степеням принадлежности.
    """
    aggregated_points = []

    for term, mu in regulator_mu_vals.items():
        points = fuzzy_set[term]
        for x, y in points:
            aggregated_points.append((x, min(mu, y)))

    return aggregated_points


def defuzzify_mamdani(aggregated_points):
    """
    Метод Мамдани: дефаззификация путем вычисления центра тяжести агрегированного множества.
    """
    aggregated_dict = {}
    for x, y in aggregated_points:
        if x in aggregated_dict:
            aggregated_dict[x] = max(aggregated_dict[x], y)
        else:
            aggregated_dict[x] = y

    # Центр тяжести
    numerator = sum(x * y for x, y in aggregated_dict.items())
    denominator = sum(y for y in aggregated_dict.values())
    return numerator / denominator if denominator != 0 else 0


def main(temperatures_json: str, regulator_json: str, transition_json: str, temperature_input: float):
    """
    Основная функция, реализующая алгоритм управления методом Мамдани.
    """
    temperatures_set = json.loads(temperatures_json)
    regulator_set = json.loads(regulator_json)
    transition_map = json.loads(transition_json)

    # Фаззификация температуры
    temperature_mu_vals = fuzz(temperature_input, temperatures_set)
    # Проекция на регулятор
    regulator_mu_vals = map_to_regulator(temperature_mu_vals, transition_map)
    # Агрегация выходных термов
    aggregated_points = aggregate_outputs(regulator_mu_vals, regulator_set)
    # Дефаззификация методом Мамдани
    optimal_control = defuzzify_mamdani(aggregated_points)

    print(f"Дефаззифицированное положение регулятора методом Мамдани: {optimal_control}\n")
    return optimal_control


# Пример данных
temperatures = """{
    "холодно": [
        [0, 1],
        [16, 1],
        [20, 0],
        [50, 0]
    ],
    "комфортно": [
        [16, 0],
        [20, 1],
        [22, 1],
        [26, 0]
    ],
    "жарко": [
        [0, 0],
        [22, 0],
        [26, 1],
        [50, 1]
    ]
}"""

regulator = """{
    "слабо": [
        [0, 1],
        [6, 1],
        [10, 0],
        [20, 0]
    ],
    "умеренно": [
        [6, 0],
        [10, 1],
        [12, 1],
        [16, 0]
    ],
    "интенсивно": [
        [0, 0],
        [12, 0],
        [16, 1],
        [20, 1]
    ]
}"""

transition = """{
    "холодно": "интенсивно",
    "комфортно": "умеренно",
    "жарко": "слабо"
}"""

# Запуск
main(temperatures, regulator, transition, 20)
