
import random
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

# ====== Настройки страницы ======
st.set_page_config(
    page_title="📏 Равномерное распределение - Анализ", 
    layout="wide"
)

# ====== Заголовок ======
st.markdown("""
<div style="
    background: linear-gradient(90deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 8px 32px rgba(255, 154, 158, 0.3);
">
    <h1 style="color: #333; margin: 0; font-size: 2.8rem; font-weight: 700;">
        📏 Анализ равномерного распределения
    </h1>
    <p style="color: #555; margin: 1rem 0 0 0; font-size: 1.3rem;">
        Статистический анализ с мерами расхождения U(a, b)
    </p>
</div>
""", unsafe_allow_html=True)

# ====== Параметры в sidebar ======
with st.sidebar:
    st.markdown("## ⚙️ Параметры распределения")

    a = st.number_input(
        "a (нижняя граница)", 
        value=0.0, 
        step=0.1, 
        format="%.4f",
        help="Минимальное значение равномерного распределения"
    )

    b = st.number_input(
        "b (верхняя граница)", 
        value=1.0, 
        step=0.1, 
        format="%.4f",
        help="Максимальное значение равномерного распределения"
    )

    N = st.number_input(
        "N (размер выборки)", 
        value=1000, 
        min_value=10, 
        max_value=10000,
        step=50,
        help="Количество генерируемых значений"
    )

    seed = st.number_input("Seed", value=42, step=1)

    if st.button("🎲 Новая выборка", type="primary"):
        st.rerun()

# ====== Проверка ======
if a >= b:
    st.error("❌ a должно быть меньше b")
    st.stop()

# ====== Генерация данных ======
random.seed(seed)
np.random.seed(seed)

# Генерация выборки из равномерного распределения
samples = [random.uniform(a, b) for _ in range(N)]

# Теоретические значения для U(a,b)
mean_theor = (a + b) / 2                    # μ = (a + b) / 2
var_theor = (b - a) ** 2 / 12              # σ² = (b - a)² / 12  
std_theor = np.sqrt(var_theor)              # σ = √σ²

# Выборочные значения
mean_sample = sum(samples) / N
var_sample = sum((x - mean_sample) ** 2 for x in samples) / N
std_sample = np.sqrt(var_sample)

# ====== МЕРЫ РАСХОЖДЕНИЯ ======
delta1 = abs(mean_sample - mean_theor)      # Расхождение по среднему
delta2 = abs(var_sample - var_theor)        # Расхождение по дисперсии  
delta3 = abs(std_sample - std_theor)        # Расхождение по ст. отклонению

# Относительные ошибки
rel_error_mean = (delta1 / abs(mean_theor) * 100) if mean_theor != 0 else (delta1 * 100)
rel_error_var = (delta2 / var_theor * 100)
rel_error_std = (delta3 / std_theor * 100)

# ====== ОТОБРАЖЕНИЕ МЕР РАСХОЖДЕНИЯ ======  
st.markdown("## 🎯 Меры расхождения")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    ">
        <h2 style="margin: 0; font-size: 1.5rem; font-weight: 600;">Δ₁</h2>
        <p style="margin: 0.5rem 0; font-size: 0.9rem; opacity: 0.9;">
            Расхождение по среднему
        </p>
        <p style="
            font-size: 2.5rem; 
            font-weight: 700; 
            margin: 1rem 0; 
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        ">
            {delta1:.8f}
        </p>
        <div style="
            background: rgba(255,255,255,0.2);
            padding: 0.5rem;
            border-radius: 10px;
            margin-top: 1rem;
        ">
            <p style="margin: 0; font-size: 0.9rem;">
                Относительная ошибка:<br>
                <strong>{rel_error_mean:.6f}%</strong>
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #f093fb, #f5576c);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(240, 147, 251, 0.3);
    ">
        <h2 style="margin: 0; font-size: 1.5rem; font-weight: 600;">Δ₂</h2>
        <p style="margin: 0.5rem 0; font-size: 0.9rem; opacity: 0.9;">
            Расхождение по дисперсии
        </p>
        <p style="
            font-size: 2.5rem; 
            font-weight: 700; 
            margin: 1rem 0;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        ">
            {delta2:.8f}
        </p>
        <div style="
            background: rgba(255,255,255,0.2);
            padding: 0.5rem;
            border-radius: 10px;
            margin-top: 1rem;
        ">
            <p style="margin: 0; font-size: 0.9rem;">
                Относительная ошибка:<br>
                <strong>{rel_error_var:.6f}%</strong>
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #4facfe, #00f2fe);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(79, 172, 254, 0.3);
    ">
        <h2 style="margin: 0; font-size: 1.5rem; font-weight: 600;">Δ₃</h2>
        <p style="margin: 0.5rem 0; font-size: 0.9rem; opacity: 0.9;">
            Расхождение по ст. откл.
        </p>
        <p style="
            font-size: 2.5rem; 
            font-weight: 700; 
            margin: 1rem 0;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        ">
            {delta3:.8f}
        </p>
        <div style="
            background: rgba(255,255,255,0.2);
            padding: 0.5rem;
            border-radius: 10px;
            margin-top: 1rem;
        ">
            <p style="margin: 0; font-size: 0.9rem;">
                Относительная ошибка:<br>
                <strong>{rel_error_std:.6f}%</strong>
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ====== ОСНОВНЫЕ МЕТРИКИ ======
st.markdown("## 📊 Основные статистики")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📈 Выборочное среднее",
        f"{mean_sample:.6f}",
        delta=f"{mean_sample - mean_theor:+.6f}",
        help=f"Теоретическое: {mean_theor:.6f}"
    )

with col2:
    st.metric(
        "📊 Выборочная дисперсия", 
        f"{var_sample:.6f}",
        delta=f"{var_sample - var_theor:+.6f}",
        help=f"Теоретическая: {var_theor:.6f}"
    )

with col3:
    st.metric(
        "📏 Выборочное ст. откл.",
        f"{std_sample:.6f}",
        delta=f"{std_sample - std_theor:+.6f}",
        help=f"Теоретическое: {std_theor:.6f}"
    )

with col4:
    st.metric(
        "🔢 Размер выборки",
        f"{N:,}",
        help="Общее количество значений"
    )

# ====== ТЕОРЕТИЧЕСКАЯ СПРАВКА ======
st.markdown("## 📚 Теоретическая информация")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    ### 📏 Равномерное распределение U({a}, {b})

    **Теоретические характеристики:**
    - Среднее значение: μ = (a + b) / 2 = **{mean_theor:.6f}**
    - Дисперсия: σ² = (b - a)² / 12 = **{var_theor:.6f}**
    - Стандартное отклонение: σ = **{std_theor:.6f}**
    - Плотность вероятности: f(x) = 1/(b-a) = **{1/(b-a):.6f}**
    - Область определения: [{a}, {b}]
    """)

with col2:
    st.markdown(f"""
    ### 📈 Выборочные характеристики

    **Рассчитано по выборке из {N} значений:**
    - Выборочное среднее: x̄ = **{mean_sample:.6f}**
    - Выборочная дисперсия: s² = **{var_sample:.6f}**
    - Выборочное ст. отклонение: s = **{std_sample:.6f}**
    - Наблюдаемый размах: [{min(samples):.6f}, {max(samples):.6f}]
    - Медиана: **{np.median(samples):.6f}**
    """)

# ====== ВИЗУАЛИЗАЦИЯ ======
st.markdown("## 📈 Визуализация")

# Создаем графики
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

# 1. Гистограмма с теоретической плотностью
n_bins = min(50, max(10, N//20))
ax1.hist(samples, bins=n_bins, density=True, alpha=0.7, color='lightcoral', edgecolor='black', label='Выборочные данные')

# Теоретическая плотность (прямоугольник)
density_theor = 1 / (b - a)
ax1.axhline(y=density_theor, color='red', linewidth=3, label=f'Теоретическая плотность = {density_theor:.4f}')
ax1.axvline(x=a, color='red', linestyle='--', alpha=0.7, label=f'Границы [{a}, {b}]')
ax1.axvline(x=b, color='red', linestyle='--', alpha=0.7)

ax1.set_title(f'Гистограмма равномерного распределения U({a}, {b})', fontsize=14, fontweight='bold')
ax1.set_xlabel('Значения')
ax1.set_ylabel('Плотность')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 2. Q-Q Plot
stats.probplot(samples, dist=stats.uniform, sparams=(a, b - a), plot=ax2)
ax2.set_title('Q-Q Plot (проверка равномерности)', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)

# 3. Временной ряд (первые 200 точек)
show_n = min(200, N)
ax3.plot(range(show_n), samples[:show_n], 'b-', alpha=0.7, linewidth=1, label='Значения выборки')
ax3.axhline(y=mean_sample, color='red', linestyle='--', label=f'Выборочное μ = {mean_sample:.4f}')
ax3.axhline(y=mean_theor, color='green', linestyle=':', label=f'Теоретическое μ = {mean_theor:.4f}')
ax3.axhline(y=a, color='orange', linestyle='-.', alpha=0.7, label=f'Границы [{a}, {b}]')
ax3.axhline(y=b, color='orange', linestyle='-.', alpha=0.7)
ax3.set_title(f'Временной ряд (первые {show_n} значений)', fontsize=14, fontweight='bold')
ax3.set_xlabel('Номер наблюдения')
ax3.set_ylabel('Значение')
ax3.legend(fontsize=8)
ax3.grid(True, alpha=0.3)

# 4. Boxplot
box_plot = ax4.boxplot(samples, vert=True, patch_artist=True, 
                      boxprops=dict(facecolor='lightblue', alpha=0.7),
                      medianprops=dict(color='black', linewidth=2))
ax4.axhline(y=mean_theor, color='green', linestyle=':', linewidth=2, label=f'Теоретическое μ = {mean_theor:.4f}')
ax4.axhline(y=a, color='red', linestyle='--', alpha=0.7, label=f'Теоретические границы')
ax4.axhline(y=b, color='red', linestyle='--', alpha=0.7)
ax4.set_title('Диаграмма размахов', fontsize=14, fontweight='bold')
ax4.set_ylabel('Значения')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
st.pyplot(fig)

# ====== ПОДРОБНАЯ СТАТИСТИКА ======
st.markdown("## 📋 Подробная статистика")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🎯 Сравнение характеристик")

    comparison_data = {
        "Характеристика": ["Среднее", "Дисперсия", "Ст. отклонение", "Плотность"],
        "Теоретическое": [
            f"{mean_theor:.8f}", 
            f"{var_theor:.8f}", 
            f"{std_theor:.8f}",
            f"{1/(b-a):.8f}"
        ],
        "Выборочное": [
            f"{mean_sample:.8f}", 
            f"{var_sample:.8f}", 
            f"{std_sample:.8f}",
            "—"
        ],
        "Абс. разность": [
            f"{delta1:.8f}", 
            f"{delta2:.8f}", 
            f"{delta3:.8f}",
            "—"
        ],
        "Отн. ошибка (%)": [
            f"{rel_error_mean:.6f}", 
            f"{rel_error_var:.6f}", 
            f"{rel_error_std:.6f}",
            "—"
        ]
    }

    st.dataframe(comparison_data, use_container_width=True, hide_index=True)

with col2:
    st.markdown("### 📊 Дополнительные статистики")

    additional_stats = {
        "Показатель": [
            "Минимум",
            "1-й квартиль", 
            "Медиана",
            "3-й квартиль",
            "Максимум",
            "Размах",
            "IQR",
            "Асимметрия"
        ],
        "Значение": [
            f"{np.min(samples):.6f}",
            f"{np.percentile(samples, 25):.6f}",
            f"{np.median(samples):.6f}",
            f"{np.percentile(samples, 75):.6f}",
            f"{np.max(samples):.6f}",
            f"{np.max(samples) - np.min(samples):.6f}",
            f"{np.percentile(samples, 75) - np.percentile(samples, 25):.6f}",
            f"{stats.skew(samples):.6f}"
        ]
    }

    st.dataframe(additional_stats, use_container_width=True, hide_index=True)

# ====== ТЕСТ НА РАВНОМЕРНОСТЬ ======
st.markdown("## 🔍 Тест на равномерность")

# Тест Колмогорова-Смирнова
ks_stat, ks_p = stats.kstest(samples, lambda x: stats.uniform.cdf(x, loc=a, scale=(b-a)))

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Статистика К-С", f"{ks_stat:.6f}")
with col2:
    st.metric("p-значение", f"{ks_p:.6f}")
with col3:
    if ks_p > 0.05:
        st.success("✅ Равномерность НЕ отвергается")
    else:
        st.error("❌ Равномерность отвергается")

# Проверка равномерности по интервалам
st.markdown("### 📊 Анализ равномерности по интервалам")

n_intervals = 10
interval_width = (b - a) / n_intervals
expected_per_interval = N / n_intervals
observed_counts = []

intervals_data = []
for i in range(n_intervals):
    left = a + i * interval_width
    right = a + (i + 1) * interval_width
    count = sum(1 for x in samples if left <= x < right)
    if i == n_intervals - 1:  # Последний интервал включает правую границу
        count += sum(1 for x in samples if x == b)

    observed_counts.append(count)
    deviation = count - expected_per_interval
    intervals_data.append({
        "Интервал": f"[{left:.3f}, {right:.3f}{'[' if i < n_intervals-1 else ']'}",
        "Наблюдаемое": count,
        "Ожидаемое": f"{expected_per_interval:.1f}",
        "Отклонение": f"{deviation:+.1f}"
    })

intervals_df = pd.DataFrame(intervals_data)
st.dataframe(intervals_df, use_container_width=True, hide_index=True)

# ====== ПЕРВЫЕ 20 ЗНАЧЕНИЙ ======
st.markdown("### 🔢 Первые 20 сгенерированных значений")

first_20 = samples[:20]
rows_data = []
for i in range(0, len(first_20), 5):
    row = first_20[i:i+5]
    while len(row) < 5:
        row.append("")
    rows_data.append([f"{val:.6f}" if val != "" else "" for val in row])

first_20_df = {f"Позиция {i+1}": [row[i] for row in rows_data] for i in range(5)}

st.dataframe(first_20_df, use_container_width=True, hide_index=True)

# ====== ИНТЕРПРЕТАЦИЯ ======
st.markdown("## 💡 Интерпретация результатов")

if all(err < 5.0 for err in [rel_error_mean, rel_error_var, rel_error_std]):
    st.success("""
    ✅ **Отличное соответствие равномерному распределению!** 

    Все относительные ошибки менее 5%, что говорит о высоком качестве генерации 
    и достаточном размере выборки для точной оценки параметров.
    """)
elif all(err < 10.0 for err in [rel_error_mean, rel_error_var, rel_error_std]):
    st.info("""
    ℹ️ **Хорошее соответствие равномерному распределению**

    Относительные ошибки в приемлемых пределах (< 10%). 
    Увеличение размера выборки может улучшить точность оценок.
    """)
else:
    st.warning("""
    ⚠️ **Значительные расхождения**

    Обнаружены относительно большие отклонения от теоретических значений. 
    Рекомендуется увеличить размер выборки или проверить параметры.
    """)

# Дополнительные проверки
if np.min(samples) < a or np.max(samples) > b:
    st.error(f"""
    🚨 **Внимание: Значения вышли за границы распределения!**

    Минимум: {np.min(samples):.6f} (должно быть ≥ {a})
    Максимум: {np.max(samples):.6f} (должно быть ≤ {b})
    """)

# ====== FOOTER ======
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; padding: 2rem;">
    <h4>📏 Анализ равномерного распределения U({a}, {b})</h4>
    <p>
        <strong>Δ₁</strong> = |x̄ - μ| — абсолютное расхождение выборочного и теоретического средних<br>
        <strong>Δ₂</strong> = |s² - σ²| — абсолютное расхождение выборочной и теоретической дисперсий<br>
        <strong>Δ₃</strong> = |s - σ| — абсолютное расхождение выборочного и теоретического стандартных отклонений
    </p>
    <p>
        <strong>Формулы для U(a,b):</strong><br>
        μ = (a + b) / 2, σ² = (b - a)² / 12, f(x) = 1 / (b - a)
    </p>
    <p><em>Создано с использованием Streamlit, NumPy, SciPy и Matplotlib</em></p>
</div>
""", unsafe_allow_html=True)
