# -*- coding: utf-8 -*-
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

import streamlit as st
import pandas as pd
import pickle

# Configuracion de la pagina
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

# Funcion para cargar el modelo
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

# Cargar modelo
model_data = cargar_modelo()

# Encabezado principal
st.markdown('<p class="main-header">Sistema de Prediccion de Rendimiento Academico</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Basado en habitos de uso de redes sociales en estudiantes universitarios peruanos</p>', unsafe_allow_html=True)

# Informacion del modelo
if model_data:
    st.markdown("""
    <div class="info-box">
        <strong>Modelo utilizado:</strong> Random Forest Classifier<br>
        <strong>Precision del modelo:</strong> ~68% en datos de prueba<br>
        <strong>Dataset:</strong> 600 estudiantes universitarios peruanos
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Formulario de entrada
st.subheader("Ingrese los datos del estudiante")

col1, col2 = st.columns(2)

with col1:
    edad = st.number_input(
        "Edad",
        min_value=16,
        max_value=35,
        value=20,
        step=1,
        help="Edad del estudiante (16-35 anos)"
    )
    
    ciclo = st.selectbox(
        "Ciclo Academico",
        options=list(range(1, 11)),
        index=2,
        help="Ciclo academico actual (1-10)"
    )
    
    horas_redes_sociales = st.slider(
        "Horas diarias en redes sociales",
        min_value=0.5,
        max_value=12.0,
        value=4.0,
        step=0.5,
        help="Promedio de horas diarias en redes sociales"
    )
    
    horas_estudio = st.slider(
        "Horas diarias de estudio",
        min_value=0.5,
        max_value=10.0,
        value=3.0,
        step=0.5,
        help="Promedio de horas diarias dedicadas al estudio"
    )
    
    red_social = st.selectbox(
        "Red social principal",
        options=['TikTok', 'WhatsApp', 'Instagram', 'Facebook', 'YouTube', 
                 'Twitter', 'Discord', 'LinkedIn', 'Telegram'],
        index=0,
        help="Red social que mas utiliza"
    )

with col2:
    motivo_uso = st.selectbox(
        "Principal motivo de uso",
        options=['Entretenimiento', 'Socializacion', 'Academico', 'Noticias', 'Trabajo'],
        index=0,
        help="Motivo principal por el que usa redes sociales"
    )
    
    afecta_concentracion = st.selectbox(
        "Las RRSS afectan tu concentracion?",
        options=['Nunca', 'Rara vez', 'A veces', 'Frecuentemente', 'Siempre'],
        index=2,
        help="Frecuencia con que las redes sociales afectan tu concentracion"
    )
    
    afecta_horas_estudio = st.selectbox(
        "Crees que las RRSS afectan tus horas de estudio?",
        options=['Si', 'No'],
        index=0,
        help="Percepcion de si las redes sociales afectan tu tiempo de estudio"
    )
    
    usa_estrategias = st.selectbox(
        "Usas estrategias para evitar distracciones?",
        options=['Si', 'No'],
        index=1,
        help="Si usas alguna estrategia para evitar distracciones de RRSS"
    )
    
    impacto_general = st.selectbox(
        "Percepcion del impacto de RRSS en tu rendimiento",
        options=['Muy Negativo', 'Negativo', 'Neutral', 'Positivo', 'Muy Positivo'],
        index=2,
        help="Tu percepcion general del impacto de las redes sociales"
    )

st.markdown("---")

# Boton de prediccion
if st.button("Predecir Rendimiento Academico", type="primary", use_container_width=True):
    
    if model_data:
        # Crear DataFrame con los datos ingresados
        input_data = pd.DataFrame({
            'Edad': [edad],
            'Ciclo': [ciclo],
            'Horas_Redes_Sociales': [horas_redes_sociales],
            'Horas_Estudio': [horas_estudio],
            'Red_Social_Principal': [red_social],
            'Motivo_Uso': [motivo_uso],
            'Afecta_Concentracion': [afecta_concentracion],
            'Afecta_Horas_Estudio': [afecta_horas_estudio],
            'Usa_Estrategias': [usa_estrategias],
            'Impacto_General': [impacto_general]
        })
        
        # Realizar prediccion
        modelo = model_data['model']
        label_encoder = model_data['label_encoder']
        
        prediccion = modelo.predict(input_data)[0]
        probabilidades = modelo.predict_proba(input_data)[0]
        
        clase_predicha = label_encoder.classes_[prediccion]
        
        # Mostrar resultado
        st.subheader("Resultado de la Prediccion")
        
        if clase_predicha == 'Alto':
            st.markdown(f"""
            <div class="result-alto">
                <p class="prediction-text" style="color: #155724;">Rendimiento Predicho: ALTO</p>
            </div>
            """, unsafe_allow_html=True)
        elif clase_predicha == 'Promedio':
            st.markdown(f"""
            <div class="result-promedio">
                <p class="prediction-text" style="color: #856404;">Rendimiento Predicho: PROMEDIO</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-bajo">
                <p class="prediction-text" style="color: #721c24;">Rendimiento Predicho: BAJO</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Mostrar probabilidades
        st.subheader("Probabilidades por categoria")
        
        # Ordenar por probabilidad
        prob_dict = {label_encoder.classes_[i]: probabilidades[i] for i in range(len(probabilidades))}
        prob_sorted = sorted(prob_dict.items(), key=lambda x: x[1], reverse=True)
        
        for clase, prob in prob_sorted:
            color = {'Alto': '#28a745', 'Promedio': '#ffc107', 'Bajo': '#dc3545'}[clase]
            st.write(f"**{clase}:** {prob*100:.1f}%")
            st.progress(prob)
        
        # Recomendaciones personalizadas
        st.subheader("Recomendaciones")
        
        if clase_predicha == 'Bajo':
            st.markdown("""
            <div class="recommendation-box">
                <strong style="color: #dc3545;">Areas de mejora sugeridas:</strong>
                <ul>
                    <li>Considere reducir el tiempo en redes sociales</li>
                    <li>Aumente las horas dedicadas al estudio</li>
                    <li>Implemente estrategias para evitar distracciones</li>
                    <li>Use las redes sociales con fines academicos</li>
                    <li>Establezca horarios fijos para el uso de RRSS</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        elif clase_predicha == 'Promedio':
            st.markdown("""
            <div class="recommendation-box">
                <strong style="color: #856404;">Sugerencias para mejorar:</strong>
                <ul>
                    <li>Mantener el equilibrio actual pero buscar optimizar</li>
                    <li>Considere reducir ligeramente el tiempo en RRSS</li>
                    <li>Incremente gradualmente las horas de estudio</li>
                    <li>Explore herramientas de productividad</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            st.markdown("""
            <div class="recommendation-box">
                <strong style="color: #28a745;">Excelente rendimiento!</strong>
                <ul>
                    <li>Continue con sus buenos habitos de estudio</li>
                    <li>Comparta sus estrategias con companeros</li>
                    <li>Mantenga el equilibrio actual</li>
                    <li>Considere actividades extracurriculares</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p><strong>Universidad Privada Antenor Orrego</strong></p>
    <p>Proyecto de Aprendizaje Estadistico - Semestre 2025-20</p>
    <p>Docente: Hernan Sagastegui Chigne</p>
</div>
""", unsafe_allow_html=True)
