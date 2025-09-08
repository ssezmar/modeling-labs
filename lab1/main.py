import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ---- Плотность и функция распределения ----
def f(x):
    return np.where((x > 0) & (x <= 1), 3*x**2, 0)

def F(x):
    return np.where(x <= 0, 0, np.where(x >= 1, 1, x**3))

# ---- Аналитические значения ----
Mx = 0.75
Dx = 0.0375

print("Mx =", Mx)
print("Dx =", Dx)

# ---- Моделирование методом обратной функции ----
def simulate(N):
    r = np.random.rand(N)
    x = r**(1/3)
    m = np.mean(x)
    g = np.mean(x**2)
    delta1 = abs(Mx - m)
    m = np.mean(x)
    hat_D = np.mean(x**2) - m**2  # выборочная дисперсия
    delta2 = abs(Dx - hat_D)

    return m, delta1, g, delta2

# ---- Создаем таблицу ----
N_values = [10, 100, 1000, 10000]
rows = []
for N in N_values:
    m, d1, g, d2 = simulate(N)
    rows.append([N, m, Mx, d1, g, Dx, d2])

df = pd.DataFrame(rows, columns=["N", "m", "Mx", "delta1", "g", "Dx", "delta2"])
print(df)

# ---- Рисуем графики f(x) и F(x) ----
x = np.linspace(-0.2, 1.2, 400)
plt.figure(figsize=(12,5))

plt.subplot(1,2,1)
plt.plot(x, f(x), label="f(x) = 3x²", color="blue")
plt.title("Плотность f(x)")
plt.grid(True)
plt.legend()

plt.subplot(1,2,2)
plt.plot(x, F(x), label="F(x) = x³", color="red")
plt.title("Функция распределения F(x)")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

# ---- Рисуем таблицу отдельным окном ----
fig, ax = plt.subplots(figsize=(10, 2.5))
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
ax.set_title("Результаты моделирования")

plt.show()
