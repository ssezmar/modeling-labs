
import random
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

# ====== Настройки страницы ======
st.set_page_config(
    page_title="🔬 Нормальное распределение - Анализ", 
    layout="wide"
)

# ====== Заголовок ======
st.markdown("""
<div style="
    background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 8px 32px rgba(79, 70, 229, 0.3);
">
    <h1 style="color: white; margin: 0; font-size: 2.8rem; font-weight: 700;">
        🔬 Анализ нормального распределения
    </h1>
    <p style="color: rgba(255,255,255,0.9); margin: 1rem 0 0 0; font-size: 1.3rem;">
        Статистический анализ с мерами расхождения
    </p>
</div>
""", unsafe_allow_html=True)

# ====== Параметры в sidebar ======
with st.sidebar:
    st.markdown("## ⚙️ Параметры")

    mu = st.number_input(
        "μ (среднее)", 
        value=0.0, 
        step=0.1, 
        format="%.4f"
    )

    sigma = st.number_input(
        "σ (стандартное отклонение)", 
        value=1.0, 
        step=0.1, 
        min_value=0.0001, 
        format="%.4f"
    )

    N = st.number_input(
        "N (размер выборки)", 
        value=1000, 
        min_value=10, 
        max_value=1000000,
        step=50
    )

    seed = st.number_input("Seed", value=42, step=1)

    if st.button("🎲 Новая выборка", type="primary"):
        st.rerun()

# ====== Проверка ======
if sigma <= 0:
    st.error("❌ σ должно быть больше 0")
    st.stop()

# ====== Генерация данных ======
random.seed(seed)
np.random.seed(seed)

# Генерация выборки
samples = [random.normalvariate(mu, sigma) for _ in range(N)]

# Теоретические значения
Mx_theor = mu
Dx_theor = sigma ** 2
sigma_theor = sigma

# Выборочные значения
m_sample = sum(samples) / N
Dx_sample = sum((x - m_sample) ** 2 for x in samples) / N
sigma_sample = np.sqrt(Dx_sample)

# ====== МЕРЫ РАСХОЖДЕНИЯ ======
delta1 = abs(m_sample - Mx_theor)          # Расхождение по среднему
delta2 = abs(Dx_sample - Dx_theor)         # Расхождение по дисперсии  
delta3 = abs(sigma_sample - sigma_theor)   # Расхождение по ст. отклонению

# Относительные ошибки
rel_error_mean = (delta1 / abs(Mx_theor) * 100) if Mx_theor != 0 else (delta1 * 100)
rel_error_var = (delta2 / Dx_theor * 100)
rel_error_std = (delta3 / sigma_theor * 100)

# ====== ОТОБРАЖЕНИЕ МER РАСХОЖДЕНИЯ ======  
st.markdown("## 🎯 Меры расхождения")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);
        transform: translateY(0);
        transition: transform 0.3s ease;
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
        background: linear-gradient(135deg, #ec4899, #be185d);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(236, 72, 153, 0.3);
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
        background: linear-gradient(135deg, #10b981, #047857);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);
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
        f"{m_sample:.6f}",
        delta=f"{m_sample - Mx_theor:+.6f}",
        help=f"Теоретическое: {Mx_theor}"
    )

with col2:
    st.metric(
        "📊 Выборочная дисперсия", 
        f"{Dx_sample:.6f}",
        delta=f"{Dx_sample - Dx_theor:+.6f}",
        help=f"Теоретическая: {Dx_theor:.6f}"
    )

with col3:
    st.metric(
        "📏 Выборочное ст. откл.",
        f"{sigma_sample:.6f}",
        delta=f"{sigma_sample - sigma_theor:+.6f}",
        help=f"Теоретическое: {sigma_theor}"
    )

with col4:
    st.metric(
        "🔢 Размер выборки",
        f"{N:,}",
        help="Общее количество значений"
    )

# ====== ВИЗУАЛИЗАЦИЯ ======
st.markdown("## 📈 Визуализация")

# Создаем графики
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

# 1. Гистограмма с теоретической кривой
ax1.hist(samples, bins=min(50, N//20), density=True, alpha=0.7, color='skyblue', edgecolor='black')
x_theory = np.linspace(min(samples), max(samples), 200)
y_theory = stats.norm.pdf(x_theory, mu, sigma)
ax1.plot(x_theory, y_theory, 'r-', linewidth=3, label=f'N({mu}, {sigma}²)')
ax1.set_title('Гистограмма с теоретической кривой', fontsize=14, fontweight='bold')
ax1.set_xlabel('Значения')
ax1.set_ylabel('Плотность')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 2. Q-Q Plot
stats.probplot(samples, dist=stats.norm, sparams=(mu, sigma), plot=ax2)
ax2.set_title('Q-Q Plot (проверка нормальности)', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)

# 3. Временной ряд (первые 200 точек)
show_n = min(200, N)
ax3.plot(range(show_n), samples[:show_n], 'b-', alpha=0.7, linewidth=1)
ax3.axhline(y=m_sample, color='red', linestyle='--', label=f'Выборочное μ = {m_sample:.4f}')
ax3.axhline(y=mu, color='green', linestyle=':', label=f'Теоретическое μ = {mu}')
ax3.set_title(f'Временной ряд (первые {show_n} значений)', fontsize=14, fontweight='bold')
ax3.set_xlabel('Номер наблюдения')
ax3.set_ylabel('Значение')
ax3.legend()
ax3.grid(True, alpha=0.3)

# 4. Boxplot
ax4.boxplot(samples, vert=True, patch_artist=True, 
           boxprops=dict(facecolor='lightcoral', alpha=0.7),
           medianprops=dict(color='black', linewidth=2))
ax4.set_title('Диаграмма размахов', fontsize=14, fontweight='bold')
ax4.set_ylabel('Значения')
ax4.grid(True, alpha=0.3)

plt.tight_layout()
st.pyplot(fig)

# ====== ПОДРОБНАЯ СТАТИСТИКА ======
st.markdown("## 📋 Подробная статистика")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🎯 Сравнение характеристик")

    comparison_data = {
        "Характеристика": ["Среднее", "Дисперсия", "Ст. отклонение"],
        "Теоретическое": [f"{Mx_theor:.8f}", f"{Dx_theor:.8f}", f"{sigma_theor:.8f}"],
        "Выборочное": [f"{m_sample:.8f}", f"{Dx_sample:.8f}", f"{sigma_sample:.8f}"],
        "Абс. разность": [f"{delta1:.8f}", f"{delta2:.8f}", f"{delta3:.8f}"],
        "Отн. ошибка (%)": [f"{rel_error_mean:.6f}", f"{rel_error_var:.6f}", f"{rel_error_std:.6f}"]
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
            "Асимметрия",
            "Эксцесс"
        ],
        "Значение": [
            f"{np.min(samples):.6f}",
            f"{np.percentile(samples, 25):.6f}",
            f"{np.median(samples):.6f}",
            f"{np.percentile(samples, 75):.6f}",
            f"{np.max(samples):.6f}",
            f"{np.max(samples) - np.min(samples):.6f}",
            f"{stats.skew(samples):.6f}",
            f"{stats.kurtosis(samples):.6f}"
        ]
    }

    st.dataframe(additional_stats, use_container_width=True, hide_index=True)

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
    ✅ **Отличное соответствие!** 

    Все относительные ошибки менее 5%, что говорит о хорошем качестве генерации случайных чисел 
    и достаточном размере выборки для оценки параметров распределения.
    """)
elif all(err < 10.0 for err in [rel_error_mean, rel_error_var, rel_error_std]):
    st.info("""
    ℹ️ **Хорошее соответствие**

    Относительные ошибки находятся в приемлемых пределах (< 10%). 
    Увеличение размера выборки может улучшить точность оценок.
    """)
else:
    st.warning("""
    ⚠️ **Значительные расхождения**

    Обнаружены относительно большие отклонения от теоретических значений. 
    Рекомендуется увеличить размер выборки или проверить параметры генерации.
    """)

# ====== FOOTER ======
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <h4>🔬 Анализ нормального распределения</h4>
    <p>
        <strong>Δ₁</strong> = |x̄ - μ| — абсолютное расхождение выборочного и теоретического средних<br>
        <strong>Δ₂</strong> = |s² - σ²| — абсолютное расхождение выборочной и теоретической дисперсий<br>
        <strong>Δ₃</strong> = |s - σ| — абсолютное расхождение выборочного и теоретического стандартных отклонений
    </p>
    <p><em>Создано с использованием Streamlit, NumPy, SciPy и Matplotlib</em></p>
</div>
""", unsafe_allow_html=True)
