import random
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

# ===== ВВОД ПАРАМЕТРОВ =====
try:
    a = float(input("Введите a (начало интервала): "))
    b = float(input("Введите b (конец интервала): "))
    N = int(input("Введите N (объём выборки): "))

    if a >= b:
        raise ValueError("❌ a должно быть меньше b")
    if N <= 0:
        raise ValueError("❌ N должно быть положительным числом")

except ValueError as e:
    print("Ошибка ввода:", e)
    exit()

# ===== ГЕНЕРАЦИЯ ВЫБОРКИ =====
samples = [random.uniform(a, b) for _ in range(N)]

# Теоретические значения
Mx = (a + b) / 2
g = ((b - a)**2) / 12

# Выборочные значения
m = sum(samples) / N
Dx = sum((x - m) ** 2 for x in samples) / N

# Δ1, Δ2
delta_m = abs(m - Mx)
delta_g = abs(Dx - g)

# Первые 20 значений (4×5)
first_20 = samples[:20]
first_20_arr = np.array(first_20).reshape(4, 5)
first_20_str = [[f"{v:.6f}" for v in row] for row in first_20_arr]

# ===== СПИСОК ПАРАМЕТРОВ =====
stats_text = [
    f"a : {a}",
    f"b : {b}",
    f"N : {N}",
    f"Δ1 : {delta_m:.6f}",
    f"Δ2 : {delta_g:.6f}"
]

# ===== СОЗДАЁМ 2 РЯДА =====
fig = make_subplots(
    rows=2, cols=1,
    row_heights=[0.4, 0.6],
    subplot_titles=("Параметры", "Первые 20 значений"),
    specs=[[{"type": "xy"}], [{"type": "table"}]]
)

# ===== РЯД 1 — текст =====
for i, line in enumerate(stats_text):
    fig.add_annotation(
        text=line,
        xref="x1", yref="y1",
        x=0, y=1 - i*0.2,
        showarrow=False,
        font=dict(size=14, family="Arial"),
        row=1, col=1
    )

# Прячем оси у текстового блока
fig.update_xaxes(visible=False, row=1, col=1)
fig.update_yaxes(visible=False, row=1, col=1)

# ===== Горизонтальная черта между параметрами и таблицей =====
fig.add_shape(
    type="line",
    x0=0, x1=1, y0=0, y1=0,
    xref="paper", yref="paper",
    line=dict(color="black", width=2)
)

# ===== РЯД 2 — таблица =====
fig.add_trace(
    go.Table(
        header=dict(values=["", "", "", "", ""],
                    fill_color="paleturquoise",
                    align="center"),
        cells=dict(values=list(map(list, zip(*first_20_str))),
                   fill_color="lavender",
                   align="center")
    ),
    row=2, col=1
)

# ===== ОБЩАЯ КОНФИГУРАЦИЯ =====
fig.update_layout(
    width=600,
    height=500,
    title_text="Равномерное распределение"
)

fig.show()