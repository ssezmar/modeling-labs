
import random
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats
import pandas as pd

# ====== Настройки страницы ======
st.set_page_config(
    page_title="Анализ нормального распределения", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====== Заголовок с красивым дизайном ======
st.markdown("""
<div style="
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
">
    <h1 style="color: white; margin: 0; font-size: 2.5rem;">
        📊 Анализ нормального распределения
    </h1>
    <p style="color: #f0f0f0; margin: 0.5rem 0 0 0; font-size: 1.2rem;">
        Исследование статистических свойств и визуализация данных
    </p>
</div>
""", unsafe_allow_html=True)

# ====== Боковая панель с параметрами ======
st.sidebar.markdown("## ⚙️ Параметры распределения")

with st.sidebar:
    st.markdown("---")
    mu = st.number_input(
        "**μ (среднее значение)**", 
        value=0.0, 
        step=0.1, 
        format="%.4f",
        help="Математическое ожидание нормального распределения"
    )

    sigma = st.number_input(
        "**σ (стандартное отклонение)**", 
        value=1.0, 
        step=0.1, 
        min_value=0.0001, 
        format="%.4f",
        help="Стандартное отклонение (должно быть > 0)"
    )

    N = st.number_input(
        "**N (размер выборки)**", 
        value=1000, 
        min_value=10, 
        max_value=10000,
        step=10,
        help="Количество генерируемых значений"
    )

    st.markdown("---")
    seed = st.number_input(
        "**Seed (для воспроизводимости)**",
        value=42,
        min_value=0,
        step=1,
        help="Зерно для генератора случайных чисел"
    )

    if st.button("🎲 Новая выборка", type="primary"):
        st.rerun()

# ====== Проверка корректности параметров ======
if sigma <= 0:
    st.error("❌ **Ошибка:** σ должно быть больше 0")
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

# Меры расхождения
delta1 = abs(m_sample - Mx_theor)
delta2 = abs(Dx_sample - Dx_theor)
delta3 = abs(sigma_sample - sigma_theor)

# Относительные ошибки (в процентах)
rel_error_mean = (delta1 / abs(Mx_theor) * 100) if Mx_theor != 0 else (delta1 * 100)
rel_error_var = (delta2 / Dx_theor * 100)
rel_error_std = (delta3 / sigma_theor * 100)

# ====== ОСНОВНЫЕ МЕТРИКИ ======
st.markdown("## 📈 Основные статистические показатели")

# Создаем 4 колонки для метрик
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📊 Размер выборки",
        value=f"{N:,}",
        help="Общее количество сгенерированных значений"
    )

with col2:
    st.metric(
        label="📐 Среднее значение",
        value=f"{m_sample:.6f}",
        delta=f"{m_sample - Mx_theor:+.6f}",
        help=f"Теоретическое: {Mx_theor}"
    )

with col3:
    st.metric(
        label="📏 Дисперсия",
        value=f"{Dx_sample:.6f}",
        delta=f"{Dx_sample - Dx_theor:+.6f}",
        help=f"Теоретическая: {Dx_theor:.6f}"
    )

with col4:
    st.metric(
        label="📊 Стандартное отклонение",
        value=f"{sigma_sample:.6f}",
        delta=f"{sigma_sample - sigma_theor:+.6f}",
        help=f"Теоретическое: {sigma_theor}"
    )

# ====== МЕРЫ РАСХОЖДЕНИЯ ======
st.markdown("## 🎯 Меры расхождения")

# Создаем карточки с мерами расхождения
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    ">
        <h3 style="margin: 0; font-size: 1.2rem;">Δ₁ (Среднее)</h3>
        <p style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0;">
            {delta1:.8f}
        </p>
        <p style="font-size: 0.9rem; opacity: 0.9; margin: 0;">
            Относительная ошибка: {rel_error_mean:.4f}%
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    ">
        <h3 style="margin: 0; font-size: 1.2rem;">Δ₂ (Дисперсия)</h3>
        <p style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0;">
            {delta2:.8f}
        </p>
        <p style="font-size: 0.9rem; opacity: 0.9; margin: 0;">
            Относительная ошибка: {rel_error_var:.4f}%
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    ">
        <h3 style="margin: 0; font-size: 1.2rem;">Δ₃ (Ст. откл.)</h3>
        <p style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0;">
            {delta3:.8f}
        </p>
        <p style="font-size: 0.9rem; opacity: 0.9; margin: 0;">
            Относительная ошибка: {rel_error_std:.4f}%
        </p>
    </div>
    """, unsafe_allow_html=True)

# ====== ВИЗУАЛИЗАЦИИ ======
st.markdown("## 📊 Визуализация данных")

# Создаем табы для разных графиков
tab1, tab2, tab3, tab4 = st.tabs(["📈 Гистограмма", "📉 Q-Q Plot", "📊 Временной ряд", "📋 Статистики"])

with tab1:
    col1, col2 = st.columns([2, 1])

    with col1:
        # Создание гистограммы с наложением теоретической кривой
        fig_hist = go.Figure()

        # Гистограмма выборочных данных
        fig_hist.add_trace(
            go.Histogram(
                x=samples,
                nbinsx=min(50, max(10, N//20)),
                name="Выборочные данные",
                opacity=0.7,
                marker_color='skyblue',
                histnorm='probability density'
            )
        )

        # Теоретическая кривая нормального распределения
        x_theory = np.linspace(min(samples), max(samples), 200)
        y_theory = stats.norm.pdf(x_theory, mu, sigma)

        fig_hist.add_trace(
            go.Scatter(
                x=x_theory,
                y=y_theory,
                mode='lines',
                name='Теоретическое N(μ={}, σ={})'.format(mu, sigma),
                line=dict(color='red', width=3)
            )
        )

        fig_hist.update_layout(
            title="Гистограмма выборки с теоретической кривой",
            xaxis_title="Значения",
            yaxis_title="Плотность вероятности",
            height=500,
            showlegend=True,
            hovermode='closest'
        )

        st.plotly_chart(fig_hist, use_container_width=True)

    with col2:
        # Статистики распределения
        st.markdown("### 📊 Статистики")

        # Вычисляем дополнительные статистики
        skewness = stats.skew(samples)
        kurtosis = stats.kurtosis(samples)

        stats_df = pd.DataFrame({
            "Показатель": [
                "Минимум",
                "25% квантиль", 
                "Медиана",
                "75% квантиль",
                "Максимум",
                "Асимметрия",
                "Эксцесс"
            ],
            "Значение": [
                f"{np.min(samples):.4f}",
                f"{np.percentile(samples, 25):.4f}",
                f"{np.median(samples):.4f}",
                f"{np.percentile(samples, 75):.4f}",
                f"{np.max(samples):.4f}",
                f"{skewness:.4f}",
                f"{kurtosis:.4f}"
            ]
        })

        st.dataframe(stats_df, use_container_width=True, hide_index=True)

with tab2:
    # Q-Q Plot для проверки нормальности
    fig_qq = go.Figure()

    # Вычисление Q-Q plot
    sorted_samples = np.sort(samples)
    n = len(sorted_samples)
    theoretical_quantiles = stats.norm.ppf(np.arange(1, n+1) / (n+1), mu, sigma)

    fig_qq.add_trace(
        go.Scatter(
            x=theoretical_quantiles,
            y=sorted_samples,
            mode='markers',
            name='Данные выборки',
            marker=dict(color='blue', size=4)
        )
    )

    # Добавляем линию y=x для идеального соответствия
    min_val = min(min(theoretical_quantiles), min(sorted_samples))
    max_val = max(max(theoretical_quantiles), max(sorted_samples))

    fig_qq.add_trace(
        go.Scatter(
            x=[min_val, max_val],
            y=[min_val, max_val],
            mode='lines',
            name='Идеальное соответствие',
            line=dict(color='red', dash='dash', width=2)
        )
    )

    fig_qq.update_layout(
        title="Q-Q Plot: Проверка соответствия нормальному распределению",
        xaxis_title="Теоретические квантили",
        yaxis_title="Выборочные квантили",
        height=500,
        showlegend=True
    )

    st.plotly_chart(fig_qq, use_container_width=True)

    # Тест Шапиро-Уилка
    if N <= 5000:  # Ограничение для теста Шапиро-Уилка
        shapiro_stat, shapiro_p = stats.shapiro(samples)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Статистика Шапиро-Уилка", f"{shapiro_stat:.6f}")
        with col2:
            st.metric("p-значение", f"{shapiro_p:.6f}")

        if shapiro_p > 0.05:
            st.success("✅ Гипотеза о нормальности НЕ отвергается (p > 0.05)")
        else:
            st.warning("⚠️ Гипотеза о нормальности отвергается (p ≤ 0.05)")

with tab3:
    # Временной ряд значений
    fig_time = go.Figure()

    # Показываем только первые 500 точек для читаемости
    show_n = min(500, N)
    indices = list(range(show_n))

    fig_time.add_trace(
        go.Scatter(
            x=indices,
            y=samples[:show_n],
            mode='lines+markers',
            name='Сгенерированные значения',
            line=dict(color='blue', width=1),
            marker=dict(size=3)
        )
    )

    # Добавляем горизонтальные линии для среднего
    fig_time.add_hline(
        y=m_sample, 
        line_dash="dash", 
        line_color="red",
        annotation_text=f"Выборочное среднее: {m_sample:.4f}"
    )

    fig_time.add_hline(
        y=mu, 
        line_dash="dot", 
        line_color="green",
        annotation_text=f"Теоретическое среднее: {mu:.4f}"
    )

    fig_time.update_layout(
        title=f"Временной ряд сгенерированных значений (первые {show_n} точек)",
        xaxis_title="Номер наблюдения",
        yaxis_title="Значение",
        height=500,
        showlegend=True
    )

    st.plotly_chart(fig_time, use_container_width=True)

with tab4:
    # Подробная таблица статистик
    st.markdown("### 📋 Сравнение теоретических и выборочных характеристик")

    comparison_df = pd.DataFrame({
        "Характеристика": [
            "Среднее значение (μ)",
            "Дисперсия (σ²)", 
            "Стандартное отклонение (σ)",
            "Минимальное значение",
            "Максимальное значение",
            "Размах",
            "Асимметрия",
            "Эксцесс"
        ],
        "Теоретическое": [
            f"{Mx_theor:.6f}",
            f"{Dx_theor:.6f}",
            f"{sigma_theor:.6f}",
            "-∞",
            "+∞", 
            "∞",
            "0.0000",
            "0.0000"
        ],
        "Выборочное": [
            f"{m_sample:.6f}",
            f"{Dx_sample:.6f}",
            f"{sigma_sample:.6f}",
            f"{np.min(samples):.6f}",
            f"{np.max(samples):.6f}",
            f"{np.max(samples) - np.min(samples):.6f}",
            f"{skewness:.6f}",
            f"{kurtosis:.6f}"
        ],
        "Абсолютная разность": [
            f"{delta1:.6f}",
            f"{delta2:.6f}",
            f"{delta3:.6f}",
            "-",
            "-",
            "-",
            f"{abs(skewness):.6f}",
            f"{abs(kurtosis):.6f}"
        ],
        "Относительная ошибка (%)": [
            f"{rel_error_mean:.4f}%",
            f"{rel_error_var:.4f}%", 
            f"{rel_error_std:.4f}%",
            "-",
            "-",
            "-",
            "-",
            "-"
        ]
    })

    st.dataframe(comparison_df, use_container_width=True, hide_index=True)

    # Таблица первых 20 значений
    st.markdown("### 🔢 Первые 20 сгенерированных значений")

    first_20 = samples[:20]
    # Разбиваем на строки по 5 значений
    rows_data = []
    for i in range(0, len(first_20), 5):
        row = first_20[i:i+5]
        # Дополняем строку пустыми значениями если нужно
        while len(row) < 5:
            row.append("")
        rows_data.append([f"{val:.6f}" if val != "" else "" for val in row])

    first_20_df = pd.DataFrame(
        rows_data,
        columns=[f"Значение {i+1}" for i in range(5)]
    )

    st.dataframe(first_20_df, use_container_width=True, hide_index=True)

# ====== FOOTER ======
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>📊 <strong>Анализ нормального распределения</strong></p>
    <p>Создано с использованием Streamlit, Plotly и SciPy</p>
</div>
""", unsafe_allow_html=True)
