import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ---- Плотность и функция распределения ----
def f(x):
    return np.where((x > 2) & (x < 5), 1 / (x * np.log(5/2)), 0)

def F(x):
    return np.where(
        x <= 2, 0,
        np.where(
            x >= 5, 1,
            np.log(x/2)/np.log(5/2)
        )
    )

# ---- Моделирование методом обратной функции ----
def simulate(N):
    r = np.random.rand(N)
    x = 2 * (5/2)**r         # обратная функция F^-1(r)
    
    m = np.mean(x)           # выборочное среднее
    g = np.mean(x**2)        # средний квадрат
    hat_D = g - m**2         # выборочная дисперсия
    
    # Mx и Dx по выборке
    Mx = m
    Dx = hat_D
    
    delta1 = 0
    delta2 = 0
    
    return m, g, hat_D

# ---- Создаем таблицу ----
N_values = [10, 100, 1000, 10000]
rows = []
for N in N_values:
    m, g, hat_D = simulate(N)
    rows.append([N, m, g, hat_D])

df = pd.DataFrame(rows, columns=["N", "m", "g", "hat_D"])
print(df)

# ---- Рисуем графики f(x) и F(x) ----
x_vals = np.linspace(1.8, 5.2, 400)
plt.figure(figsize=(12,5))

plt.subplot(1,2,1)
plt.plot(x_vals, f(x_vals), label="f(x) = 1/(x ln(5/2))", color="blue")
plt.title("Плотность f(x)")
plt.grid(True)
plt.legend()

plt.subplot(1,2,2)
plt.plot(x_vals, F(x_vals), label="F(x)", color="red")
plt.title("Функция распределения F(x)")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

# ---- Рисуем таблицу отдельным окном ----
fig, ax = plt.subplots(figsize=(12, 2.5))
ax.axis("off")
table = ax.table(
    cellText=df.round(6).values,
    colLabels=df.columns,
    loc="center",
    cellLoc="center"
)
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.5)
ax.set_title("Результаты моделирования (Mx и Dx по выборке)", fontweight="bold")
plt.show()
