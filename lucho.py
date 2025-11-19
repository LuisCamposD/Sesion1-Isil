import streamlit as st
import random

# ------------------ CONFIGURACIÓN BÁSICA ------------------ #
st.set_page_config(page_title="Ecuaciones de primer grado", page_icon="🧮")

# URL de la imagen del BCP en tu repo GitHub (ajusta si cambias el nombre)
BCP_BG_URL = "https://raw.githubusercontent.com/LuisCamposD/Sesion1-Isil/main/bcp.jpg"

page_bg = f"""
<style>
.stApp {{
    background-image:
        linear-gradient(rgba(0,0,0,0.35), rgba(0,0,0,0.70)),
        url("{BCP_BG_URL}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}

h1, h2, h3, h4, h5, h6, p, label {{
    color: #F4F4F4 !important;
}}

.main-card {{
    background: rgba(15, 23, 42, 0.94);
    padding: 2rem;
    border-radius: 1.2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}}

.stButton>button {{
    border-radius: 0.6rem;
    padding: 0.6rem 1.2rem;
    border: none;
    font-weight: 600;
}}

.stNumberInput input {{
    border-radius: 0.5rem;
}}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ------------------ PARÁMETROS DEL JUEGO ------------------ #
MAX_ATTEMPTS = 10
MAX_SCORE = 100
POINTS_PER_CORRECT = MAX_SCORE // MAX_ATTEMPTS  # 10
POINTS_PENALTY_WRONG = 5

# ------------------ FUNCIONES AUXILIARES ------------------ #
def generar_ecuacion(dificultad: str):
    """Genera una ecuación de primer grado ax + b = c según el nivel."""
    if dificultad == "Fácil":
        a = random.randint(1, 5)
        x_real = random.randint(-10, 10)
        b = random.randint(-10, 10)
    elif dificultad == "Medio":
        a = random.randint(2, 10)
        x_real = random.randint(-15, 15)
        b = random.randint(-20, 20)
    else:  # Difícil
        a = random.randint(3, 15)
        x_real = random.randint(-20, 20)
        b = random.randint(-30, 30)

    c = a * x_real + b
    return {"a": a, "b": b, "c": c, "x_real": x_real}


def reset_game():
    """Reinicia puntaje, intentos y ecuación."""
    st.session_state.score = 0
    st.session_state.attempts_left = MAX_ATTEMPTS
    st.session_state.equation = generar_ecuacion(st.session_state.difficulty)


# ------------------ ESTADO INICIAL ------------------ #
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Fácil"

if "score" not in st.session_state:
    st.session_state.score = 0

if "attempts_left" not in st.session_state:
    st.session_state.attempts_left = MAX_ATTEMPTS

if "equation" not in st.session_state:
    st.session_state.equation = generar_ecuacion(st.session_state.difficulty)

# ------------------ UI PRINCIPAL ------------------ #
st.markdown('<div class="main-card">', unsafe_allow_html=True)

st.title("🧮 Taller de Ecuaciones de Primer Grado")
st.write(
    "Tienes **10 intentos** para lograr el puntaje máximo de **100 puntos**.\n\n"
    "- Respuesta correcta: **+10 puntos** (dependa del intento).\n"
    "- Respuesta incorrecta: **−5 puntos**.\n"
    "- Cuando aciertas, verás **aplausos y celebración** 👏🎉"
)

# --- Selección de dificultad --- #
niveles = ["Fácil", "Medio", "Difícil"]
nivel_seleccionado = st.radio(
    "Nivel de dificultad:",
    niveles,
    index=niveles.index(st.session_state.difficulty),
    horizontal=True,
)

# Si cambian el nivel, reiniciamos el juego
if nivel_seleccionado != st.session_state.difficulty:
    st.session_state.difficulty = nivel_seleccionado
    reset_game()
    st.rerun()

# --- Mostrar marcador --- #
col_score, col_attempts = st.columns(2)
with col_score:
    st.metric("Puntaje", f"{st.session_state.score} / {MAX_SCORE}")
with col_attempts:
    st.metric("Intentos restantes", st.session_state.attempts_left)

st.progress((MAX_ATTEMPTS - st.session_state.attempts_left) / MAX_ATTEMPTS)

st.markdown("---")

# --- Mostrar ecuación actual --- #
eq = st.session_state.equation
a, b, c, x_real = eq["a"], eq["b"], eq["c"], eq["x_real"]

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

col1, col2, col3 = st.columns(3)

with col1:
    verificar = st.button("✔ Verificar resultado")

with col2:
    nueva_ecuacion = st.button("🔁 Nueva ecuación")

with col3:
    nueva_partida = st.button("🆕 Nueva partida (reiniciar)")

# ------------------ LÓGICA DE BOTONES ------------------ #
# Nueva partida
if nueva_partida:
    reset_game()
    st.rerun()

# Nueva ecuación sin resetear puntaje/ intentos
if nueva_ecuacion:
    st.session_state.equation = generar_ecuacion(st.session_state.difficulty)
    st.rerun()

# Verificar resultado
if verificar:
    if st.session_state.attempts_left <= 0:
        st.warning("Ya usaste tus 10 intentos. Inicia una **nueva partida** para seguir jugando.")
    else:
        st.session_state.attempts_left -= 1

        if abs(x_usuario - x_real) < 1e-6:
            # Correcto
            st.session_state.score = min(
                MAX_SCORE, st.session_state.score + POINTS_PER_CORRECT
            )
            st.success(f"✅ ¡Resultado correcto! x = {x_real} 👏👏👏")
            st.balloons()  # celebración tipo aplausos
        else:
            # Incorrecto
            st.session_state.score = max(
                0, st.session_state.score - POINTS_PENALTY_WRONG
            )
            st.error("❌ Aún no es correcto. Pierdes 5 puntos, intenta otra vez 😉")

        # Si ya se acabaron los intentos, mensaje final
        if st.session_state.attempts_left == 0:
            st.info(
                f"🏁 Fin de la partida. Tu puntaje final es **{st.session_state.score} / {MAX_SCORE}**.\n\n"
                "Haz clic en **'Nueva partida'** para volver a empezar."
            )

st.markdown('</div>', unsafe_allow_html=True)
