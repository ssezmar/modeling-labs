"""
assignment_7_8.py
Решение задания 7.8 (СМО с отказами) для одноканальной и многоканальной систем.
При запуске выводит таблицу показателей Q и A через matplotlib.
"""


import math
import pandas as pd
import matplotlib.pyplot as plt


# Параметры задачи
LAMBDA = 90.0  # интенсивность поступления заявок, заявок/час
SERVICE_TIME_MIN = 2.0  # среднее время обслуживания, мин
MU = 60.0 / SERVICE_TIME_MIN  # интенсивность обслуживания, заявок/час
RHO = LAMBDA / MU  # приведенная интенсивность нагрузки


# Функция для одноканальной системы
def single_channel_metrics(lambda_, mu):
    p0 = mu / (lambda_ + mu)
    Q = p0
    A = lambda_ * Q
    return {'n': 1, 'Q': Q, 'A': A}


# Функция для многоканальной системы по формулам Эрланга
def multi_channel_metrics(lambda_, mu, rho, n):
    # нормировочная сумма
    sum_term = sum((rho ** k) / math.factorial(k) for k in range(n+1))
    p0 = 1.0 / sum_term
    # вероятность отказа (рассчитывается, но не возвращается)
    P_reject = (rho ** n / math.factorial(n)) * p0
    Q = 1.0 - P_reject
    A = lambda_ * Q
    return {'n': n, 'Q': Q, 'A': A}


# Основная логика
def main():
    results = []
    # Одноканальная система
    results.append(single_channel_metrics(LAMBDA, MU))
    # Многоканальные от 2 до 6
    for n in range(2, 7):
        results.append(multi_channel_metrics(LAMBDA, MU, RHO, n))


    # Создаем DataFrame для отображения
    df_display = pd.DataFrame(results)
    df_display.columns = ['Каналы (n)', 'Q', 'A (заявок/ч)']
    # Форматирование процентов для красивого отображения в таблице
    df_display['Q'] = df_display['Q'].map(lambda x: f"{x:.3f} ({x*100:.1f}%)")
    df_display['A (заявок/ч)'] = df_display['A (заявок/ч)'].map(lambda x: f"{x:.1f}")

    # === Создаем фигуру и оси только для таблицы ===
    fig, ax = plt.subplots(figsize=(8, 3)) # Подбираем размер под таблицу
    ax.axis('tight')
    ax.axis('off') # Отключаем оси для таблицы

    table = ax.table(
        cellText=df_display.values,
        colLabels=df_display.columns,
        cellLoc='center',
        loc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.8) # Растягиваем ячейки по вертикали для лучшей читаемости
    ax.set_title('Показатели эффективности СМО с отказами (задача 7.8)', fontsize=12, pad=20)

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
