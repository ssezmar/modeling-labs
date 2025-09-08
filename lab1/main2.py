import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ---- Плотность и функция распределения ----
def f(x):
    return np.where((x > 0.5) & (x < np.sqrt(3)/2),
                    6 / (np.pi * np.sqrt(1 - x**2)),
                    0)

def F(x):
    # функция распределения через arcsin
    return np.where(
        x <= 0.5, 0,
        np.where(
            x >= np.sqrt(3)/2, 1,
            (6/np.pi) * (np.arcsin(x) - np.pi/6)
        )
    )

# ---- Аналитические значения ----
Mx = (3/np.pi) * (np.sqrt(3) - 1)
Ex2 = 0.5
Dx = Ex2 - Mx**2

print("Mx =", Mx)
print("Dx =", Dx)

# ---- Моделирование методом обратной функции ----
def simulate(N):
    r = np.random.rand(N)
    x = np.sin((np.pi/6) * (1 + r))  # обратная функция F^-1(r)
    m = np.mean(x)                    # выборочное среднее
    g = np.mean(x**2)                 # средний квадрат
    hat_D = g - m**2                  # выборочная дисперсия
    delta1 = abs(Mx - m)
    delta2 = abs(Dx - hat_D)
    return m, delta1, g, hat_D, delta2

# ---- Создаем таблицу ----
N_values = [10, 100, 1000, 10000]
rows = []
for N in N_values:
    m, d1, g, hat_D, d2 = simulate(N)
    rows.append([N, m, Mx, d1, g, Dx, d2])

df = pd.DataFrame(rows, columns=["N", "m", "Mx", "delta1", "g", "Dx", "delta2"])
print(df)

# ---- Рисуем графики f(x) и F(x) ----
x_vals = np.linspace(0.45, 0.9, 400)
plt.figure(figsize=(12,5))

plt.subplot(1,2,1)
plt.plot(x_vals, f(x_vals), label="f(x) = 6/(π√(1-x²))", color="blue")
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
fig, ax = plt.subplots(figsize=(12, 3))
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
ax.set_title("Результаты моделирования", fontweight="bold")
plt.show()
