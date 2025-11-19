import streamlit as st
import random

st.set_page_config(page_title="Ecuaciones de primer grado", page_icon="🧮")

st.title("🧮 Resolución de ecuaciones de primer grado")
st.write("Resuelve la ecuación y comprueba si tu resultado es correcto.")

# --- Generar una ecuación y guardarla en la sesión ---
if "equation" not in st.session_state:
    a = random.randint(1, 10)          # coeficiente de x
    b = random.randint(-10, 10)        # término independiente
    x_real = random.randint(-10, 10)   # solución real
    c = a * x_real + b                 # lado derecho
    st.session_state.equation = {"a": a, "b": b, "c": c, "x_real": x_real}

eq = st.session_state.equation
a, b, c, x_real = eq["a"], eq["b"], eq["c"], eq["x_real"]

# Armamos el texto de la ecuación bonito (sin "+ -3")
if b >= 0:
    ecuacion_texto = f"{a}·x + {b} = {c}"
else:
    ecuacion_texto = f"{a}·x - {abs(b)} = {c}"

st.subheader(f"Ecuación:")
st.latex(fr"{a}x + ({b}) = {c}")
st.write(f"En forma más amigable: **{ecuacion_texto}**")

st.markdown("---")

# --- Campo para que el usuario ingrese el resultado ---
st.write("Ingresa el valor de **x** que crees que resuelve la ecuación:")

x_usuario = st.number_input(
    "Tu respuesta para x:",
    step=0.1,
    format="%.2f",
    key="respuesta_x"
)

col1, col2 = st.columns(2)

with col1:
    verificar = st.button("✔ Verificar resultado")

with col2:
    nueva = st.button("🔁 Nueva ecuación")

# --- Lógica para verificar ---
if verificar:
    # permitimos un pequeño margen de error por decimales
    if abs(x_usuario - x_real) < 1e-6:
        st.success(f"✅ ¡Resultado correcto! x = {x_real} 😄")
    else:
        st.error("❌ Aún no es correcto. Vuelve a intentarlo 😉")

# --- Botón para generar una nueva ecuación ---
if nueva:
    a = random.randint(1, 10)
    b = random.randint(-10, 10)
    x_real = random.randint(-10, 10)
    c = a * x_real + b
    st.session_state.equation = {"a": a, "b": b, "c": c, "x_real": x_real}
    st.experimental_rerun()
