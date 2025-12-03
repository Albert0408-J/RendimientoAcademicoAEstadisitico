"""
================================================================================
SISTEMA DE PREDICCION DE RENDIMIENTO ACADEMICO
================================================================================
Proyecto: Relacion entre uso de redes sociales y rendimiento academico
Universidad: Universidad Privada Antenor Orrego
Curso: Aprendizaje Estadistico - Semestre 2025-20
================================================================================
"""

from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd
import streamlit as st
import pickle

st.set_page_config(
    page_title="Sistema de Prediccion - Rendimiento Academico",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="collapsed"
)

CSS_PATH = Path(__file__).resolve().parent / "styles" / "main.css"


def load_custom_css() -> None:
    if CSS_PATH.exists():
        css = CSS_PATH.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    else:
        st.warning("No se encontró el archivo de estilos en styles/main.css")


load_custom_css()

SOCIAL_NETWORKS: Tuple[str, ...] = (
    "TikTok",
    "WhatsApp",
    "Instagram",
    "Facebook",
    "YouTube",
    "Twitter",
    "Discord",
    "LinkedIn",
    "Telegram",
)

MOTIVOS_USO: Tuple[str, ...] = (
    "Entretenimiento",
    "Socializacion",
    "Academico",
    "Noticias",
    "Trabajo",
)

FRECUENCIA_IMPACTO: Tuple[str, ...] = (
    "Nunca",
    "Rara vez",
    "A veces",
    "Frecuentemente",
    "Siempre",
)

RESPUESTA_BINARIA: Tuple[str, ...] = ("Si", "No")

IMPACTO_GENERAL: Tuple[str, ...] = (
    "Muy Negativo",
    "Negativo",
    "Neutral",
    "Positivo",
    "Muy Positivo",
)

RESULT_CARD_META = {
    "Alto": {"css": "result-alto", "color": "#155724", "label": "ALTO"},
    "Promedio": {"css": "result-promedio", "color": "#856404", "label": "PROMEDIO"},
    "Bajo": {"css": "result-bajo", "color": "#721c24", "label": "BAJO"},
}

RECOMMENDATIONS = {
    "Bajo": {
        "color": "#dc3545",
        "title": "Areas de mejora sugeridas",
        "items": [
            "Considere reducir el tiempo en redes sociales",
            "Aumente las horas dedicadas al estudio",
            "Implemente estrategias para evitar distracciones",
            "Use las redes sociales con fines academicos",
            "Establezca horarios fijos para el uso de RRSS",
        ],
    },
    "Promedio": {
        "color": "#856404",
        "title": "Sugerencias para mejorar",
        "items": [
            "Mantener el equilibrio actual pero buscar optimizar",
            "Considere reducir ligeramente el tiempo en RRSS",
            "Incremente gradualmente las horas de estudio",
            "Explore herramientas de productividad",
        ],
    },
    "Alto": {
        "color": "#28a745",
        "title": "Excelente rendimiento!",
        "items": [
            "Continue con sus buenos habitos de estudio",
            "Comparta sus estrategias con companeros",
            "Mantenga el equilibrio actual",
            "Considere actividades extracurriculares",
        ],
    },
}


def render_header(model_loaded: bool) -> None:
    st.markdown('<p class="main-header">Sistema de Prediccion de Rendimiento Academico</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Basado en habitos de uso de redes sociales en estudiantes universitarios peruanos</p>',
        unsafe_allow_html=True,
    )

    if model_loaded:
        st.markdown(
            """
            <div class="info-box">
                <strong>Modelo utilizado:</strong> Random Forest Classifier<br>
                <strong>Precision del modelo:</strong> ~68% en datos de prueba<br>
                <strong>Dataset:</strong> 600 estudiantes universitarios peruanos
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")


def render_form() -> Dict[str, float | int | str]:
    st.subheader("Ingrese los datos del estudiante")
    col1, col2 = st.columns(2)

    with col1:
        edad = st.number_input(
            "Edad",
            min_value=16,
            max_value=35,
            value=20,
            step=1,
            help="Edad del estudiante (16-35 anos)",
        )
        ciclo = st.selectbox(
            "Ciclo Academico",
            options=list(range(1, 11)),
            index=2,
            help="Ciclo academico actual (1-10)",
        )
        horas_redes_sociales = st.slider(
            "Horas diarias en redes sociales",
            min_value=0.5,
            max_value=12.0,
            value=4.0,
            step=0.5,
            help="Promedio de horas diarias en redes sociales",
        )
        horas_estudio = st.slider(
            "Horas diarias de estudio",
            min_value=0.5,
            max_value=10.0,
            value=3.0,
            step=0.5,
            help="Promedio de horas diarias dedicadas al estudio",
        )
        red_social = st.selectbox(
            "Red social principal",
            options=SOCIAL_NETWORKS,
            index=0,
            help="Red social que mas utiliza",
        )

    with col2:
        motivo_uso = st.selectbox(
            "Principal motivo de uso",
            options=MOTIVOS_USO,
            index=0,
            help="Motivo principal por el que usa redes sociales",
        )
        afecta_concentracion = st.selectbox(
            "Las RRSS afectan tu concentracion?",
            options=FRECUENCIA_IMPACTO,
            index=2,
            help="Frecuencia con que las redes sociales afectan tu concentracion",
        )
        afecta_horas_estudio = st.selectbox(
            "Crees que las RRSS afectan tus horas de estudio?",
            options=RESPUESTA_BINARIA,
            index=0,
            help="Percepcion de si las redes sociales afectan tu tiempo de estudio",
        )
        usa_estrategias = st.selectbox(
            "Usas estrategias para evitar distracciones?",
            options=RESPUESTA_BINARIA,
            index=1,
            help="Si usas alguna estrategia para evitar distracciones de RRSS",
        )
        impacto_general = st.selectbox(
            "Percepcion del impacto de RRSS en tu rendimiento",
            options=IMPACTO_GENERAL,
            index=2,
            help="Tu percepcion general del impacto de las redes sociales",
        )

    st.markdown("---")

    return {
        "Edad": edad,
        "Ciclo": ciclo,
        "Horas_Redes_Sociales": horas_redes_sociales,
        "Horas_Estudio": horas_estudio,
        "Red_Social_Principal": red_social,
        "Motivo_Uso": motivo_uso,
        "Afecta_Concentracion": afecta_concentracion,
        "Afecta_Horas_Estudio": afecta_horas_estudio,
        "Usa_Estrategias": usa_estrategias,
        "Impacto_General": impacto_general,
    }


def run_prediction(model_data: Dict[str, object], features: Dict[str, object]) -> Tuple[str, List[Tuple[str, float]]]:
    input_data = pd.DataFrame({key: [value] for key, value in features.items()})
    modelo = model_data["model"]
    label_encoder = model_data["label_encoder"]

    prediccion = modelo.predict(input_data)[0]
    probabilidades = modelo.predict_proba(input_data)[0]

    prob_dict = {
        str(label_encoder.classes_[i]): float(prob)
        for i, prob in enumerate(probabilidades)
    }

    prob_sorted = sorted(prob_dict.items(), key=lambda item: item[1], reverse=True)
    return str(label_encoder.classes_[prediccion]), prob_sorted


def render_prediction_result(predicted_label: str) -> None:
    meta = RESULT_CARD_META.get(predicted_label, RESULT_CARD_META["Promedio"])
    st.subheader("Resultado de la Prediccion")
    st.markdown(
        f"""
        <div class="{meta['css']}">
            <p class="prediction-text" style="color: {meta['color']};">Rendimiento Predicho: {meta['label']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_probabilities(probabilities: List[Tuple[str, float]]) -> None:
    st.subheader("Probabilidades por categoria")
    for label, prob in probabilities:
        st.write(f"**{label}:** {prob * 100:.1f}%")
        st.progress(prob)


def render_recommendations(predicted_label: str) -> None:
    st.subheader("Recomendaciones")
    config = RECOMMENDATIONS.get(predicted_label, RECOMMENDATIONS["Promedio"])
    items_html = "".join(f"<li>{item}</li>" for item in config["items"])

    st.markdown(
        f"""
        <div class="recommendation-box">
            <strong style="color: {config['color']};">{config['title']}</strong>
            <ul>{items_html}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

@st.cache_resource
def cargar_modelo():
    try:
        with open('modelo_rendimiento_academico.pkl', 'rb') as f:
            model_data = pickle.load(f)
        return model_data
    except FileNotFoundError:
        st.error("Error: No se encontro el archivo del modelo 'modelo_rendimiento_academico.pkl'")
        st.info("Asegurese de que el archivo del modelo este en el mismo directorio que esta aplicacion.")
        return None


def main() -> None:
    model_data = cargar_modelo()
    render_header(model_data is not None)
    features = render_form()

    if st.button("Predecir Rendimiento Academico", type="primary", use_container_width=True):
        if not model_data:
            st.error("No se puede realizar la prediccion sin el modelo cargado.")
            return

        predicted_label, probabilities = run_prediction(model_data, features)
        render_prediction_result(predicted_label)
        render_probabilities(probabilities)
        render_recommendations(predicted_label)

    st.markdown("""
    <div class="footer">
        <p><strong>Universidad Privada Antenor Orrego</strong></p>
        <p>Proyecto de Aprendizaje Estadistico - Semestre 2025-20</p>
        <p>Docente: Hernan Sagastegui Chigne</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
