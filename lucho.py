import streamlit as st
import random

# ------------------ CONFIGURACIÓN BÁSICA ------------------ #
st.set_page_config(page_title="Ecuaciones de primer grado", page_icon="🧮")

# CSS para fondo con temática de pizarra + estilos
page_bg = """
<style>
.stApp {
    background-image:
        linear-gradient(rgba(0,0,0,0.60), rgba(0,0,0,0.75)),
        url("https://images.unsplash.com/photo-1523580846011-d3a5bc25702b");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Quitar color sólido del header */
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

/* Color de los textos principales */
h1, h2, h3, h4, h5, h6, p, label {
    color: #F4F4F4 !important;
}

/* Tarjeta central semi-transparente */
.main-card {
    background: rgba(15, 23, 42, 0.92); /* azul oscuro semi-transparente */
    padding: 2rem;
    border-radius: 1.2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
}

/* Botones más bonitos */
.stButton>button {
    border-radius: 0.6rem;
    padding: 0.6rem 1.2rem;
    border: none;
    font-weight: 600;
}

/* Inputs redondeados */
.stNumberInput input {
    border-radius: 0.5rem;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ------------------ LÓGICA DE LA APLICACIÓN ------------------ #

st.markdown('<div class="main-card">', unsafe_allow_html=True)

st.title("🧮 Taller de Ecuaciones de Primer Grado")
st.write("Resuelve la ecuación y comprueba si tu respuesta es correcta. "
         "Si aciertas, aparecerá un emoticón de aprobación 😄")

# Generar una ecuación y guardarla en la sesión
if "equation" not in st.session_state:
    a = random.randint(1, 10)          # coeficiente de x
    b = random.randint(-10, 10)        # término independiente
    x_real = random.randint(-10, 10)   # solución real
    c = a * x_real + b                 # lado derecho
    st.session_state.equation = {"a": a, "b": b, "c": c, "x_real": x_real}

eq = st.session_state.equation
a, b, c, x_real = eq["a"], eq["b"], eq["c"], eq["x_real"]

# Texto de la ecuación
if b >= 0:
    ecuacion_texto = f"{a}·x + {b} = {c}"
else:
    ecuacion_texto = f"{a}·x - {abs(b)} = {c}"

st.subheader("✨ Tu ecuación")
st.latex(fr"{a}x + ({b}) = {c}")
st.write(f"En formato más amigable: **{ecuacion_texto}**")

st.markdown("---")

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

# Verificar resultado
if verificar:
    if abs(x_usuario - x_real) < 1e-6:
        st.success(f"✅ ¡Resultado correcto! x = {x_real} 😄")
    else:
        st.error("❌ Aún no es correcto. Vuelve a intentarlo 😉")

# Generar nueva ecuación
if nueva:
    a = random.randint(1, 10)
    b = random.randint(-10, 10)
    x_real = random.randint(-10, 10)
    c = a * x_real + b
    st.session_state.equation = {"a": a, "b": b, "c": c, "x_real": x_real}
    st.experimental_rerun()

st.markdown('</div>', unsafe_allow_html=True)

