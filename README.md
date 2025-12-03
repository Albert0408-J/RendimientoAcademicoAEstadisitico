# Proyecto de Aprendizaje Estadistico

## Relacion entre el uso de redes sociales y la productividad academica en estudiantes universitarios peruanos

### Universidad Privada Antenor Orrego - Semestre 2025-20
**Docente:** Hernan Sagastegui Chigne

---

## Descripcion del Proyecto

Este proyecto analiza la relacion entre el uso de redes sociales y el rendimiento academico en estudiantes universitarios peruanos, utilizando tecnicas de Machine Learning para predecir el rendimiento academico basandose en los habitos de uso de redes sociales.

### Hallazgos Principales

- **Correlacion negativa significativa (r = -0.682)** entre horas de uso de redes sociales y rendimiento academico
- **Correlacion positiva fuerte (r = 0.739)** entre horas de estudio y rendimiento academico
- El promedio de uso de redes sociales es de **4.5 horas diarias**
- El modelo Random Forest logro una exactitud de **71%** en datos de prueba

---

## Estructura del Repositorio

```
/
├── Proyecto_RRSS_Rendimiento_Colab.ipynb  # Notebook para Google Colab
├── app.py                                   # Aplicacion Streamlit
├── modelo_rendimiento_academico.pkl         # Modelo entrenado
├── dataset_rrss_rendimiento_limpio.xlsx     # Dataset limpio (600 estudiantes)
├── requirements.txt                         # Dependencias
├── Informe_Proyecto_Aprendizaje_Estadistico.docx  # Informe completo
├── grafico_1_distribucion.png               # Graficos generados
├── grafico_2_correlaciones.png
├── grafico_3_analisis_categorico.png
├── grafico_4_matriz_confusion.png
├── grafico_5_importancia_features.png
└── README.md
```

---

## 7.1.1 Documentacion del Proyecto

### Dataset

- **Tamano:** 600 estudiantes universitarios peruanos
- **Variables:** 16 (demograficas, uso de RRSS, habitos de estudio, rendimiento)
- **Variable objetivo:** Rendimiento_Academico (Alto, Promedio, Bajo)

### Variables Principales

| Variable | Tipo | Descripcion |
|----------|------|-------------|
| Horas_Redes_Sociales | Numerica | Horas diarias en RRSS (0.5-12) |
| Horas_Estudio | Numerica | Horas diarias de estudio (0.5-10) |
| Red_Social_Principal | Categorica | TikTok, WhatsApp, Instagram, etc. |
| Motivo_Uso | Categorica | Entretenimiento, Academico, etc. |
| Rendimiento_Academico | Categorica | Alto, Promedio, Bajo |

### Distribucion de Clases

- **Promedio:** 241 estudiantes (40.17%)
- **Alto:** 210 estudiantes (35.00%)
- **Bajo:** 149 estudiantes (24.83%)

---

## 7.1.2 Codigo del Sistema

### Archivos de Codigo

1. **Proyecto_RRSS_Rendimiento_Colab.ipynb**
   - Notebook completo para Google Colab
   - Incluye generacion de datos, limpieza, EDA, entrenamiento y evaluacion
   - 15 secciones documentadas

2. **app.py**
   - Aplicacion web con Streamlit
   - Interfaz interactiva para predicciones
   - Sin emojis, diseno profesional

3. **modelo_rendimiento_academico.pkl**
   - Modelo Random Forest serializado
   - Incluye pipeline de preprocesamiento
   - Listo para produccion

### Tecnologias Utilizadas

- Python 3.x
- scikit-learn 1.3.0
- pandas 2.1.0
- Streamlit 1.28.0
- matplotlib, seaborn

---

## 7.1.3 Ejecucion y Pruebas del Sistema

### Opcion 1: Google Colab (Recomendado para desarrollo)

1. Abrir `Proyecto_RRSS_Rendimiento_Colab.ipynb` en Google Colab
2. Ejecutar todas las celdas secuencialmente (Runtime > Run all)
3. El notebook generara automaticamente:
   - Dataset de 600 estudiantes
   - Modelo entrenado
   - 6 graficos de analisis
   - Metricas de evaluacion

### Opcion 2: Ejecucion Local

```bash
# Clonar repositorio
git clone https://github.com/Albert0408-J/RendimientoAcademicoAEstadisitico.git
cd RendimientoAcademicoAEstadisitico

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicacion web
streamlit run app.py
```

### Opcion 3: Aplicacion Web Desplegada

Acceder directamente a la aplicacion desplegada (si esta disponible):
- URL del deploy: [Pendiente de configurar]

---

## 7.2 Deploy del Sistema de Prediccion

### Caracteristicas de la Aplicacion Web

- **Framework:** Streamlit 1.28.0
- **Modelo:** Random Forest Classifier
- **Precision:** 71% en datos de prueba

### Funcionalidades
2
1. **Ingreso de datos del estudiante:**
   - Edad, Ciclo academico
   - Horas en redes sociales
   - Horas de estudio
   - Red social principal
   - Motivo de uso
   - Percepcion de impacto

2. **Prediccion:**
   - Clasificacion: Alto, Promedio, Bajo
   - Probabilidades por categoria
   - Visualizacion con barras de progreso

3. **Recomendaciones personalizadas:**
   - Sugerencias segun el resultado
   - Areas de mejora identificadas

---

## Resultados del Modelo

### Validacion Cruzada (K-Fold, k=10)

| Modelo | CV Accuracy |
|--------|-------------|
| Decision Tree | 71% |

### Importancia de Caracteristicas (Top 5)

1. Horas_Estudio: 25.8%
2. Horas_Redes_Sociales: 22.2%
3. Ciclo: 7.7%
4. Edad: 6.5%
5. Motivo_Uso_Academico: 3.5%

---

## Referencias

- Estudio UNAP (2024). Tendencias en el uso de redes sociales entre estudiantes universitarios en una institucion andina del Peru.
- Universidad Peruana Los Andes (2023). Rendimiento academico y uso de redes sociales en estudiantes de pregrado.
- Scielo Peru (2019). Uso de redes sociales por estudiantes de pregrado de una facultad de medicina en Lima.

---

## Autores

**Equipo de Proyecto - UPAO 2025-20**

- Torres Avalos, Joaquin (Coordinador)
- Y 7 integrantes adicionales

---

## Licencia

Este proyecto fue desarrollado con fines academicos para el curso de Aprendizaje Estadistico.
