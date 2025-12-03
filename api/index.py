"""
================================================================================
API DE PREDICCION DE RENDIMIENTO ACADEMICO - VERCEL
================================================================================
Proyecto: Relacion entre uso de redes sociales y rendimiento academico
Universidad: Universidad Privada Antenor Orrego
Curso: Aprendizaje Estadistico - Semestre 2025-20
================================================================================
"""

from flask import Flask, request, render_template, jsonify
import numpy as np
import pandas as pd
import pickle
import os
import urllib.request
from pathlib import Path

app = Flask(__name__, template_folder='templates')

MODEL_URL = os.environ.get(
    'MODEL_URL',
    'https://raw.githubusercontent.com/Albert0408-J/RendimientoAcademicoAEstadisitico/staging/api/modelo_rendimiento_academico.pkl'
)

FEATURE_ORDER = [
    'Edad', 'Ciclo', 'Horas_Redes_Sociales', 'Horas_Estudio',
    'Red_Social_Principal', 'Motivo_Uso', 'Afecta_Concentracion',
    'Afecta_Horas_Estudio', 'Usa_Estrategias', 'Impacto_General'
]

def cargar_modelo():
    """Carga el modelo desde URL externa o archivo local."""
    local_path = Path(__file__).parent / 'modelo_rendimiento_academico.pkl'
    if local_path.exists():
        try:
            with open(local_path, 'rb') as f:
                return pickle.load(f)
        except Exception:
            pass
    
    try:
        with urllib.request.urlopen(MODEL_URL, timeout=10) as response:
            return pickle.load(response)
    except Exception as e:
        print(f"Error cargando modelo: {e}")
        return None

model_data = cargar_modelo()

SOCIAL_NETWORKS = [
    "TikTok", "WhatsApp", "Instagram", "Facebook", 
    "YouTube", "Twitter", "Discord", "LinkedIn", "Telegram"
]

MOTIVOS_USO = [
    "Entretenimiento", "Socializacion", "Academico", 
    "Noticias", "Trabajo"
]

FRECUENCIA_IMPACTO = [
    "Nunca", "Rara vez", "A veces", "Frecuentemente", "Siempre"
]

RESPUESTA_BINARIA = ["Si", "No"]

IMPACTO_GENERAL = [
    "Muy Negativo", "Negativo", "Neutral", "Positivo", "Muy Positivo"
]

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

def run_prediction(model_data, features):
    """Ejecuta prediccion usando pandas DataFrame (requerido por ColumnTransformer)."""
    modelo = model_data["model"]
    label_encoder = model_data["label_encoder"]
    
    input_data = pd.DataFrame({key: [value] for key, value in features.items()})
    
    prediccion = modelo.predict(input_data)[0]
    probabilidades = modelo.predict_proba(input_data)[0]

    prob_dict = {
        str(label_encoder.classes_[i]): float(prob)
        for i, prob in enumerate(probabilidades)
    }

    prob_sorted = sorted(prob_dict.items(), key=lambda item: item[1], reverse=True)
    return str(label_encoder.classes_[prediccion]), prob_sorted

@app.route('/health')
def health():
    if model_data:
        return jsonify({'status': 'ok', 'model_loaded': True})
    else:
        return jsonify({'status': 'error', 'model_loaded': False}), 500

@app.route('/')
def index():
    return render_template('index.html', 
                         social_networks=SOCIAL_NETWORKS,
                         motivos_uso=MOTIVOS_USO,
                         frecuencia_impacto=FRECUENCIA_IMPACTO,
                         respuesta_binaria=RESPUESTA_BINARIA,
                         impacto_general=IMPACTO_GENERAL)

@app.route('/predict', methods=['POST'])
def predict():
    if not model_data:
        return jsonify({'error': 'Modelo no disponible'}), 500
    
    try:
        features = {
            'Edad': int(request.form['edad']),
            'Ciclo': int(request.form['ciclo']),
            'Horas_Redes_Sociales': float(request.form['horas_redes_sociales']),
            'Horas_Estudio': float(request.form['horas_estudio']),
            'Red_Social_Principal': request.form['red_social_principal'],
            'Motivo_Uso': request.form['motivo_uso'],
            'Afecta_Concentracion': request.form['afecta_concentracion'],
            'Afecta_Horas_Estudio': request.form['afecta_horas_estudio'],
            'Usa_Estrategias': request.form['usa_estrategias'],
            'Impacto_General': request.form['impacto_general'],
        }
        
        predicted_label, probabilities = run_prediction(model_data, features)
        recommendations = RECOMMENDATIONS.get(predicted_label, RECOMMENDATIONS["Promedio"])
        
        return jsonify({
            'prediction': predicted_label,
            'probabilities': probabilities,
            'recommendations': recommendations
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
