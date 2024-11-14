import numpy as np
from math import log2

def entropy(probs):
    """Функция для вычисления энтропии распределения вероятностей."""
    return -np.sum([p * log2(p) for p in probs if p > 0])

def joint_entropy(joint_probs):
    """Функция для вычисления энтропии совместного распределения вероятностей."""
    return -np.sum([p * log2(p) for row in joint_probs for p in row if p > 0])

def process(data):
    """Ваша оригинальная функция для расчета энтропии и количества информации."""
    mat = np.array(data)
    total = mat.sum()

    prob_matrix = mat / total
    p_y = prob_matrix.sum(axis=1)  # Вероятности по строкам
    p_x = prob_matrix.sum(axis=0)  # Вероятности по столбцам

    H_joint = entropy(prob_matrix.flatten())
    H_age = entropy(p_y)
    H_product = entropy(p_x)

    cond_prob_matrix = np.copy(prob_matrix)
    H_cond = 0
    for i in range(len(prob_matrix)):
        cond_prob_matrix[i] /= p_y[i]
        H_i = entropy(cond_prob_matrix[i])
        H_cond += H_i * p_y[i]

    info_gain = H_product - H_cond

    print("="*40)
    print(f"Количество информации (I): {round(info_gain, 2)}")
    print(f"Энтропия совместного события (H): {round(H_age + H_cond, 2)} (проверка: {round(H_joint, 2)})")
    print("="*40)

def calculate_probabilities():
    """Функция для расчёта вероятностей суммы и произведения чисел на двух кубиках."""
    outcomes = [(i + 1, j + 1) for i in range(6) for j in range(6)]

    sums = {s: 0 for s in range(2, 13)}
    products = {p: 0 for p in range(1, 37)}
    joint_counts = {(s, p): 0 for s in sums for p in products}

    for a, b in outcomes:
        sum_ab = a + b
        product_ab = a * b
        sums[sum_ab] += 1
        products[product_ab] += 1
        joint_counts[(sum_ab, product_ab)] += 1

    total_outcomes = len(outcomes)
    p_sum = {k: v / total_outcomes for k, v in sums.items()}
    p_product = {k: v / total_outcomes for k, v in products.items()}
    p_joint = {k: v / total_outcomes for k, v in joint_counts.items()}

    return p_sum, p_product, p_joint

def calculate_dice_entropy():
    """Функция для расчёта энтропий и количества информации для задачи с двумя кубиками."""
    p_sum, p_product, p_joint = calculate_probabilities()

    prob_sum = list(p_sum.values())
    prob_product = list(p_product.values())
    prob_joint = np.array([list(p_joint[(s, p)] for p in p_product.keys()) for s in p_sum.keys()])

    H_A = entropy(prob_sum)
    H_B = entropy(prob_product)
    H_AB = joint_entropy(prob_joint)

    H_B_given_A = sum(entropy([p_joint[(s, p)] / p_sum[s] for p in p_product.keys() if p_joint[(s, p)] > 0]) * p_sum[s]
                      for s in p_sum.keys())

    I_AB = H_B - H_B_given_A

    return [round(H_AB, 2), round(H_A, 2), round(H_B, 2), round(H_B_given_A, 2), round(I_AB, 2)]

def main():

    test_data = [[20, 15, 10, 5],
                 [30, 20, 15, 10],
                 [25, 25, 20, 15],
                 [20, 20, 25, 20],
                 [15, 15, 30, 25]]
    
    process(test_data)

    dice_entropy_result = calculate_dice_entropy()
    print(f"Результаты для задачи с кубиками: {dice_entropy_result}")
    return dice_entropy_result

# Запуск основной функции
if __name__ == "__main__":
    main()
