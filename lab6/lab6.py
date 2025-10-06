import random
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd


# ====== Настройки страницы ======
st.set_page_config(
    page_title="📊 Анализ распределений с критерием Пирсона", 
    layout="wide"
)


# ====== Заголовок ======
st.markdown("""
<div style="
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
">
    <h1 style="color: white; margin: 0; font-size: 2.8rem; font-weight: 700;">
        📊 Анализ распределений
    </h1>
    <p style="color: rgba(255,255,255,0.9); margin: 1rem 0 0 0; font-size: 1.3rem;">
        Критерий хи-квадрат Пирсона для проверки согласия
    </p>
</div>
""", unsafe_allow_html=True)


# ====== Выбор типа распределения ======
distribution_type = st.selectbox(
    "🎯 Выберите тип распределения:",
    ["Нормальное распределение N(μ, σ²)", "Равномерное распределение U(a, b)"],
    index=0
)


# ====== Параметры в sidebar ======
with st.sidebar:
    st.markdown("## ⚙️ Параметры")

    if "Нормальное" in distribution_type:
        st.markdown("### 📈 Нормальное распределение")
        mu = st.number_input("μ (среднее)", value=0.0, step=0.1, format="%.4f")
        sigma = st.number_input("σ (стандартное отклонение)", value=1.0, step=0.1, min_value=0.0001, format="%.4f")

        if sigma <= 0:
            st.error("❌ σ должно быть больше 0")
            st.stop()
    else:
        st.markdown("### 📏 Равномерное распределение")
        a = st.number_input("a (нижняя граница)", value=0.0, step=0.1, format="%.4f")
        b = st.number_input("b (верхняя граница)", value=1.0, step=0.1, format="%.4f")

        if a >= b:
            st.error("❌ a должно быть меньше b")
            st.stop()

    N = st.number_input("N (размер выборки)", value=1000, min_value=50, max_value=10000, step=50)
    n_bins = st.number_input("Количество интервалов", value=10, min_value=5, max_value=30, step=1)
    seed = st.number_input("Seed", value=42, step=1)

    if st.button("🎲 Новая выборка", type="primary"):
        st.rerun()


# ====== Генерация данных ======
random.seed(seed)
np.random.seed(seed)

if "Нормальное" in distribution_type:
    samples = [random.normalvariate(mu, sigma) for _ in range(N)]

    mean_theor = mu
    var_theor = sigma ** 2
    std_theor = sigma

    distribution_name = f"N({mu}, {sigma}²)"

else:
    samples = [random.uniform(a, b) for _ in range(N)]

    mean_theor = (a + b) / 2
    var_theor = (b - a) ** 2 / 12
    std_theor = np.sqrt(var_theor)

    distribution_name = f"U({a}, {b})"


mean_sample = sum(samples) / N
var_sample = sum((x - mean_sample) ** 2 for x in samples) / N
std_sample = np.sqrt(var_sample)


# ====== МЕРЫ РАСХОЖДЕНИЯ ======
delta1 = abs(mean_sample - mean_theor)
delta2 = abs(var_sample - var_theor)
delta3 = abs(std_sample - std_theor)

rel_error_mean = (delta1 / abs(mean_theor) * 100) if mean_theor != 0 else (delta1 * 100)
rel_error_var = (delta2 / var_theor * 100)
rel_error_std = (delta3 / std_theor * 100)


# ====== ОТОБРАЖЕНИЕ МЕР РАСХОЖДЕНИЯ ======
st.markdown("## 🎯 Меры расхождения")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
    ">
        <h3 style="margin: 0; font-size: 1.3rem;">Δ₁</h3>
        <p style="margin: 0.3rem 0; font-size: 0.8rem; opacity: 0.9;">Расхождение по среднему</p>
        <p style="font-size: 2rem; font-weight: 700; margin: 0.5rem 0;">{delta1:.8f}</p>
        <p style="font-size: 0.8rem; opacity: 0.9;">Относительная ошибка: {rel_error_mean:.4f}%</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #ec4899, #be185d);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 8px 25px rgba(236, 72, 153, 0.3);
    ">
        <h3 style="margin: 0; font-size: 1.3rem;">Δ₂</h3>
        <p style="margin: 0.3rem 0; font-size: 0.8rem; opacity: 0.9;">Расхождение по дисперсии</p>
        <p style="font-size: 2rem; font-weight: 700; margin: 0.5rem 0;">{delta2:.8f}</p>
        <p style="font-size: 0.8rem; opacity: 0.9;">Относительная ошибка: {rel_error_var:.4f}%</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #10b981, #047857);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3);
    ">
        <h3 style="margin: 0; font-size: 1.3rem;">Δ₃</h3>
        <p style="margin: 0.3rem 0; font-size: 0.8rem; opacity: 0.9;">Расхождение по ст. откл.</p>
        <p style="font-size: 2rem; font-weight: 700; margin: 0.5rem 0;">{delta3:.8f}</p>
        <p style="font-size: 0.8rem; opacity: 0.9;">Относительная ошибка: {rel_error_std:.4f}%</p>
    </div>
    """, unsafe_allow_html=True)


# ====== КРИТЕРИЙ ХИ-КВАДРАТ ПИРСОНА ======
st.markdown("## 📊 Критерий хи-квадрат Пирсона")

observed_freq, bin_edges = np.histogram(samples, bins=n_bins)

if "Нормальное" in distribution_type:
    expected_prob = np.diff(stats.norm.cdf(bin_edges, loc=mu, scale=sigma))
    expected_freq = expected_prob * N
else:
    expected_freq = np.full(n_bins, N / n_bins)

expected_freq = expected_freq * np.sum(observed_freq) / np.sum(expected_freq)

chi2_stat = sum((observed_freq[i] - expected_freq[i])**2 / expected_freq[i] 
                for i in range(len(observed_freq)) if expected_freq[i] > 0)

degrees_of_freedom = n_bins - 1
p_value = 1 - stats.chi2.cdf(chi2_stat, degrees_of_freedom)
critical_value = stats.chi2.ppf(0.95, degrees_of_freedom)


# ====== ФОРМУЛА ======
st.markdown("""
### 📐 Формула критерия хи-квадрат Пирсона

Статистика критерия согласия Пирсона вычисляется по формуле:
""")

st.latex(r"\chi^2 = \sum_{i=1}^{m} \frac{(n_i - N p_i)^2}{N p_i}")

st.markdown("""
где:
- **m** — количество интервалов (классов)
- **n_i** — наблюдаемая частота в i-том интервале
- **N** — общий размер выборки
- **p_i** — теоретическая вероятность попадания в i-тый интервал
- **N p_i** — ожидаемая частота в i-том интервале
""")


# ====== РЕЗУЛЬТАТЫ КРИТЕРИЯ ======
col1, col2 = st.columns([2, 1])

with col1:
    fig, ax = plt.subplots(figsize=(10, 6))

    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    width = bin_edges[1] - bin_edges[0]

    ax.bar(bin_centers, observed_freq, width=width*0.8, alpha=0.7, 
           color='skyblue', edgecolor='black', label='Наблюдаемые частоты')
    ax.bar(bin_centers, expected_freq, width=width*0.4, alpha=0.8, 
           color='red', edgecolor='darkred', label='Ожидаемые частоты')

    if "Нормальное" in distribution_type:
        x_theory = np.linspace(min(samples), max(samples), 200)
        y_theory = stats.norm.pdf(x_theory, mu, sigma) * N * width
        ax.plot(x_theory, y_theory, 'g-', linewidth=2, label=f'Теоретическая кривая {distribution_name}')
    else:
        density_theor = N * width / (b - a)
        ax.axhline(y=density_theor, color='green', linewidth=2, 
                  label=f'Теоретическая плотность = {density_theor:.1f}')
        ax.axvline(x=a, color='green', linestyle='--', alpha=0.7)
        ax.axvline(x=b, color='green', linestyle='--', alpha=0.7)

    ax.set_title(f'Критерий Пирсона: {distribution_name}', fontsize=16, fontweight='bold')
    ax.set_xlabel('Значения')
    ax.set_ylabel('Частота')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.markdown("### 📊 Результаты теста")

    st.metric("χ² статистика", f"{chi2_stat:.6f}")
    st.metric("p-значение", f"{p_value:.6f}")
    st.metric("Степени свободы", degrees_of_freedom)
    st.metric("Критическое значение (α=0.05)", f"{critical_value:.6f}")

    if p_value > 0.05:
        st.success("""✅ **НЕ ОТВЕРГАЕМ H₀**

Данные соответствуют теоретическому распределению
""")
    else:
        st.error("""❌ **ОТВЕРГАЕМ H₀**

Данные НЕ соответствуют теоретическому распределению
""")


# ====== ТАБЛИЦА ЧАСТОТ ======
st.markdown("### 📋 Таблица частот по интервалам")

intervals_data = []
for i in range(n_bins):
    left_edge = bin_edges[i]
    right_edge = bin_edges[i + 1]
    observed = observed_freq[i]
    expected = expected_freq[i]
    contribution = (observed - expected)**2 / expected if expected > 0 else 0

    intervals_data.append({
        "Интервал": f"[{left_edge:.3f}, {right_edge:.3f}{'[' if i < n_bins-1 else ']'}",
        "Наблюдаемая частота (n_i)": observed,
        "Ожидаемая частота (Np_i)": f"{expected:.2f}",
        "Разность (n_i - Np_i)": f"{observed - expected:+.2f}",
        "Вклад в χ²": f"{contribution:.6f}"
    })

intervals_df = pd.DataFrame(intervals_data)
st.dataframe(intervals_df, use_container_width=True, hide_index=True)

total_chi2 = sum(float(row["Вклад в χ²"]) for row in intervals_data)
st.markdown(f"**Сумма вкладов:** {total_chi2:.6f} (должна равняться χ² = {chi2_stat:.6f})")


# ====== ОСНОВНЫЕ СТАТИСТИКИ ======
st.markdown("## 📈 Основные статистики")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📊 Выборочное среднее", f"{mean_sample:.6f}", 
              delta=f"{mean_sample - mean_theor:+.6f}")

with col2:
    st.metric("📏 Выборочная дисперсия", f"{var_sample:.6f}", 
              delta=f"{var_sample - var_theor:+.6f}")

with col3:
    st.metric("📐 Выборочное ст. откл.", f"{std_sample:.6f}", 
              delta=f"{std_sample - std_theor:+.6f}")

with col4:
    st.metric("🔢 Размер выборки", f"{N:,}")


# ====== СРАВНИТЕЛЬНАЯ ТАБЛИЦА ======
st.markdown("### 🎯 Сравнение теоретических и выборочных характеристик")

if "Нормальное" in distribution_type:
    theoretical_params = f"μ = {mu:.4f}, σ² = {sigma**2:.4f}, σ = {sigma:.4f}"
else:
    theoretical_params = f"μ = (a+b)/2 = {mean_theor:.4f}, σ² = (b-a)²/12 = {var_theor:.4f}, σ = {std_theor:.4f}"

comparison_data = {
    "Характеристика": ["Среднее значение", "Дисперсия", "Стандартное отклонение"],
    "Теоретическое": [f"{mean_theor:.8f}", f"{var_theor:.8f}", f"{std_theor:.8f}"],
    "Выборочное": [f"{mean_sample:.8f}", f"{var_sample:.8f}", f"{std_sample:.8f}"],
    "Абсолютная разность": [f"{delta1:.8f}", f"{delta2:.8f}", f"{delta3:.8f}"],
    "Относительная ошибка (%)": [f"{rel_error_mean:.4f}", f"{rel_error_var:.4f}", f"{rel_error_std:.4f}"]
}

comparison_df = pd.DataFrame(comparison_data)
st.dataframe(comparison_df, use_container_width=True, hide_index=True)

st.markdown(f"**Теоретические параметры {distribution_name}:** {theoretical_params}")


# ====== ИНТЕРПРЕТАЦИЯ ======
st.markdown("## 💡 Интерпретация результатов")

if p_value > 0.05 and all(err < 10.0 for err in [rel_error_mean, rel_error_var, rel_error_std]):
    st.success("""
✅ **Отличные результаты!**

- Критерий хи-квадрат Пирсона НЕ отвергает гипотезу о соответствии данных теоретическому распределению
- Все относительные ошибки менее 10%, что говорит о хорошем качестве генерации
- Размер выборки достаточен для надежной оценки параметров распределения
""")
elif p_value > 0.05:
    st.info("""
ℹ️ **Хорошие результаты**

- Критерий Пирсона НЕ отвергает гипотезу о соответствии распределению
- Некоторые статистические характеристики имеют заметные отклонения
- Рекомендуется увеличить размер выборки для повышения точности
""")
else:
    st.warning("""
⚠️ **Гипотеза отвергается**

- Критерий хи-квадрат Пирсона отвергает гипотезу о соответствии данных теоретическому распределению
- Возможные причины: недостаточный размер выборки, неподходящие параметры распределения
- Рекомендуется проверить параметры генерации или увеличить размер выборки
""")


# ====== FOOTER ======
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; padding: 1.5rem;">
    <h4>📊 Анализ распределения {distribution_name}</h4>
    <p>
        <strong>Критерий хи-квадрат Пирсона</strong> проверяет гипотезу H₀ о том, что выборка 
        соответствует заданному теоретическому распределению
    </p>
    <p>
        <strong>Δ₁, Δ₂, Δ₃</strong> — абсолютные расхождения выборочных и теоретических характеристик
    </p>
    <p><em>Создано с использованием Streamlit, NumPy, SciPy и Matplotlib</em></p>
</div>
""", unsafe_allow_html=True)
