import numpy as np
from math import log2

def entropy(probs):
    h = 0
    for p in np.nditer(probs):
        h -= p * log2(p)
    return h

def process(data):
    
    mat = np.array(data)

    total = mat.sum()

    prob_matrix = mat / total

    p_y = prob_matrix.sum(axis=1)  # Вероятности по возрастам
    p_x = prob_matrix.sum(axis=0)  # Вероятности по товарам
    
    H_joint = entropy(prob_matrix)
    H_age = entropy(p_y)
    H_product = entropy(p_x)
    
    cond_prob_matrix = np.copy(prob_matrix)
    H_cond = 0
    
    for i in range(len(prob_matrix)):
        cond_prob_matrix[i] /= p_y[i]
        H_i = entropy(cond_prob_matrix[i])    
        H_cond += H_i * p_y[i]

    info_gain = H_product - H_cond

    H_check = H_age + H_cond  # Должно совпадать с H_joint

    print("="*40)
    print(f"Количество информации (I): {round(info_gain, 2)}")
    print(f"Энтропия совместного события (H): {round(H_check, 2)} (проверка: {round(H_joint, 2)})")
    print("="*40)

test_data = [[20, 15, 10, 5],
             [30, 20, 15, 10],
             [25, 25, 20, 15],
             [20, 20, 25, 20],
             [15, 15, 30, 25]]

process(test_data)
