import random
import numpy as np
import streamlit as st

# ====== Настройки страницы ======
st.set_page_config(page_title="Равномерное распределение", layout="centered")
st.markdown(
    "<h1 style='text-align: center; color: #4C78A8;'>📊 Равномерное распределение</h1>",
    unsafe_allow_html=True
)

# ====== Стили для маленьких инпутов без стрелок ======
st.markdown("""
<style>
/* Уменьшаем ширину инпутов */
input[type=number] {
    width: 90px !important;
}

/* Прячем стрелочки для Chrome, Safari, Edge */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

/* Прячем стрелочки для Firefox */
input[type=number] {
    -moz-appearance: textfield;
}
</style>
""", unsafe_allow_html=True)

# ====== Инпуты в одну строку с placeholder ======
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    a = st.number_input("", value=2.0, step=0.1, format="%.2f", placeholder="a")
with col2:
    b = st.number_input("", value=5.0, step=0.1, format="%.2f", placeholder="b")
with col3:
    N = st.number_input("", value=100, min_value=1, step=1, placeholder="N")

# ====== Проверка ======
if a >= b:
    st.error("❌ a должно быть меньше b")
else:
    # ====== Генерация выборки ======
    samples = [random.uniform(a, b) for _ in range(N)]

    # Теоретические значения
    Mx = (a + b) / 2
    g = ((b - a) ** 2) / 12

    # Выборочные значения
    m = sum(samples) / N
    Dx = sum((x - m) ** 2 for x in samples) / N

    # Δ1, Δ2
    delta_m = abs(m - Mx)
    delta_g = abs(Dx - g)

    # ====== Вывод Δ1 и Δ2 в одну строку ======
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f"""
            <div style="
                text-align:center;
                padding:15px;
                background-color:#F5F9FF;
                border:2px solid #4C78A8;
                border-radius:10px;
                font-size:18px;">
                <b>Δ1:</b> {delta_m:.6f}
            </div>
            """,
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            f"""
            <div style="
                text-align:center;
                padding:15px;
                background-color:#F5F9FF;
                border:2px solid #4C78A8;
                border-radius:10px;
                font-size:18px;">
                <b>Δ2:</b> {delta_g:.6f}
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown("---")

    # ====== Таблица ======
    first_20 = samples[:20]
    first_20_arr = np.array(first_20).reshape(4, 5)
    first_20_str = [[f"{v:.6f}" for v in row] for row in first_20_arr]

    table_html = """
    <style>
    table {
        border-collapse: collapse;
        width: 100%;
        font-size: 14px;
    }
    th {
        background-color: #4C78A8;
        color: white;
        padding: 8px;
        text-align: center;
        border: 1px solid #ddd;
    }
    td {
        padding: 8px;
        border: 1px solid #ddd;
        text-align: center;
    }
    tr:nth-child(even) {
        background-color: #f2f2f2;
    }
    </style>
    <h3 style="color:#4C78A8;">📋 Первые 20 значений</h3>
    <table>
        <tr>
    """

    # Заголовки столбцов
    for j in range(5):
        table_html += f"<th>Колонка {j+1}</th>"
    table_html += "</tr>"

    # Данные
    for row in first_20_str:
        table_html += "<tr>" + "".join(f"<td>{val}</td>" for val in row) + "</tr>"

    table_html += "</table>"

    st.markdown(table_html, unsafe_allow_html=True)