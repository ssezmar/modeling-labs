import random
import matplotlib.pyplot as plt

# ---- Ввод данных ----
x = list(map(float, input("Введите значения X через пробел: ").split()))
p = list(map(float, input("Введите вероятности P через пробел: ").split()))
N = int(input("Введите N (размер выборки): "))
q = int(input("Введите q (кол-во первых значений для вывода): "))

# ---- Нормализация вероятностей ----
if abs(sum(p) - 1.0) > 1e-6:
    print("⚠️ Сумма вероятностей не равна 1, нормализуем.")
    p = [pi / sum(p) for pi in p]

# ---- Строим ключи (кумулятивные вероятности) ----
cumulative = []
s = 0
for pi in p:
    s += pi
    cumulative.append(s)

print("\nКлючи (кумулятивные вероятности):", cumulative)

# ---- Теоретические Mx и g ----
Mx = sum(xi * pi for xi, pi in zip(x, p))
g = sum((xi ** 2) * pi for xi, pi in zip(x, p)) - Mx ** 2

# ---- Функции моделирования ----
def simulate_once(x, cumulative):
    u = random.random()
    for i, c in enumerate(cumulative):
        if u < c:
            return x[i], u, i
    return x[-1], u, len(cumulative) - 1

def simulate_samples_with_counts(x, cumulative, n_samples):
    counts = [0] * len(x)  # Количество попаданий для каждого диапазона
    samples = []
    for _ in range(n_samples):
        value, u, idx = simulate_once(x, cumulative)
        samples.append(value)
        counts[idx] += 1
    return samples, counts

def compute_m_dx(samples):
    N = len(samples)
    m = sum(samples) / N
    m2 = sum([s ** 2 for s in samples]) / N
    Dx = m2 - m ** 2
    return m, Dx

# ---- Генерация выборки и счётчик попаданий ----
samples, counts = simulate_samples_with_counts(x, cumulative, N)

# ---- Вывод первых q значений ----
first_q = samples[:q]
print(f"\nПервые {q} значений выборки:")
print(first_q)

# ---- Вывод количества попаданий в диапазоны ----
print("\nКоличество попаданий в каждый диапазон (K):")
for i, c in enumerate(counts):
    range_start = 0 if i == 0 else cumulative[i-1]
    range_end = cumulative[i]
    print(f"{i+1}) Диапазон [{range_start:.4f}, {range_end:.4f}) → {c} попаданий")

# ---- Вычисляем характеристики ----
m, Dx = compute_m_dx(samples)
delta_m = abs(m - Mx)
delta_g = abs(Dx - g)

# ---- Создаём фигуру ----
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
ax1.axis('off')
ax2.axis('off')

# ---- Таблица результатов ----
header = ["N", "Mx (теор.)", "m (выбор.)", "Δm", "g (теор.)", "Dx (выбор.)", "Δg"]
table_data = [header]
table_data.append([
    N,
    f"{Mx:.6f}",
    f"{m:.6f}",
    f"{delta_m:.6f}",
    f"{g:.6f}",
    f"{Dx:.6f}",
    f"{delta_g:.6f}"
])
table = ax1.table(cellText=table_data, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1.2, 1.5)
ax1.set_title("Результаты моделирования", fontsize=12)

# ---- Блок текста с данными ----
text_lines = [
    "Условие:",
    f"X: {x}",
    f"P: {p}",
    "",
    "Ключи (кумулятивные вероятности):",
    f"{[round(c,4) for c in cumulative]}",
    "",
    f"K (количество попаданий): {counts}",
    "",
    f"Первые {q} значений выборки:",
    f"{first_q}"
]
ax2.text(0, 1, "\n".join(text_lines), va='top', fontsize=10, family='monospace')
ax2.set_title("Условие и данные", fontsize=12)

plt.tight_layout()
plt.show()