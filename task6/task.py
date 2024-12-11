import json

def membership(value, points):
    """
    Рассчитывает степень принадлежности значения value для заданной функции принадлежности.
    """
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        if x1 <= value <= x2:
            # Линейная интерполяция между точками
            return y1 + (value - x1) * (y2 - y1) / (x2 - x1)
    return 0

def defuzzify(control_values):
    """
    Центроидный метод дефаззификации.
    """
    numerator = 0
    denominator = 0
    for value, degree in control_values:
        numerator += value * degree
        denominator += degree
    return numerator / denominator if denominator != 0 else 0

def main(temperature_json, heating_json, rules_json, current_temperature):
    """
    Реализует алгоритм нечеткого управления.
    
    :param temperature_json: JSON-строка с описанием функций принадлежности температуры.
    :param heating_json: JSON-строка с описанием функций принадлежности уровня нагрева.
    :param rules_json: JSON-строка с описанием правил.
    :param current_temperature: Текущее значение температуры (градусы Цельсия).
    :return: Вещественное число значения оптимального управления.
    """
    # Парсим входные данные
    temperature_sets = json.loads(temperature_json)["температура"]
    heating_sets = json.loads(heating_json)["температура"]
    rules = json.loads(rules_json)
    
    # Вычисляем степень принадлежности текущей температуры каждому терму
    temperature_degrees = {}
    for term in temperature_sets:
        term_id = term["id"]
        term_points = term["points"]
        temperature_degrees[term_id] = membership(current_temperature, term_points)
    
    # Применяем правила для вычисления выходных значений
    control_values = []
    for rule in rules:
        temperature_term, heating_term = rule
        degree = temperature_degrees.get(temperature_term, 0)
        for heating in heating_sets:
            if heating["id"] == heating_term:
                for i in range(len(heating["points"]) - 1):
                    x1, y1 = heating["points"][i]
                    x2, y2 = heating["points"][i + 1]
                    if degree > 0:
                        # Максимальное пересечение
                        control_values.append((x1, min(y1, degree)))
                        control_values.append((x2, min(y2, degree)))
    
    # Дефаззификация
    optimal_control = defuzzify(control_values)
    print(optimal_control)
    return optimal_control

temperature_json = '''
{
  "температура": [
      {"id": "холодно", "points": [[0,1],[18,1],[22,0],[50,0]]},
      {"id": "комфортно", "points": [[18,0],[22,1],[24,1],[26,0]]},
      {"id": "жарко", "points": [[0,0],[24,0],[26,1],[50,1]]}
  ]
}
'''

heating_json = '''
{
  "температура": [
      {"id": "слабый", "points": [[0,0],[0,1],[5,1],[8,0]]},
      {"id": "умеренный", "points": [[5,0],[8,1],[13,1],[16,0]]},
      {"id": "интенсивный", "points": [[13,0],[18,1],[23,1],[26,0]]}
  ]
}
'''

rules_json = '''
[
    ["холодно", "интенсивный"],
    ["комфортно", "умеренный"],
    ["жарко", "слабый"]
]
'''

current_temperature = 20.0

main(temperature_json, heating_json, rules_json, current_temperature)
