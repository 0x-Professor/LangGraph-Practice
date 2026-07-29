# Ejemplos Prácticos de LangGraph

Este repositorio contiene ejemplos prácticos de diferentes patrones de flujo de trabajo implementados utilizando LangGraph. Cada ejemplo demuestra un tipo específico de flujo de trabajo que puede utilizarse para diversas tareas de procesamiento de datos y automatización.

## Tabla de Contenidos

- [Descripción General](#overview)
- [Ejemplos de Flujos de Trabajo](#workflow-examples)
- [Instalación](#installation)
- [Dependencias Comunes](#common-dependencies)
- [Uso](#usage)
- [Contribución](#contributing)
- [Licencia](#license)

## Descripción General

LangGraph es una biblioteca poderosa para crear y gestionar flujos de trabajo en Python. Este repositorio proporciona ejemplos prácticos de diferentes patrones de flujo de trabajo que pueden servir como referencia o punto de partida para sus propios proyectos.

## Ejemplos de Flujos de Trabajo

| Tipo de Flujo | Descripción | Ejemplo |
|--------------|-------------|---------|
| [Sequential](sequentialWorkflow) | Procesamiento lineal de datos a través de una serie de pasos | Calculadora de IMC |
| [Conditional](ConditionalWorkflow) | Lógica de ramificación basada en condiciones | Solucionador de Ecuaciones Cuadráticas, Análisis de Sentimiento |
| [Iterative](IterativeWorkflow) | Procesamiento repetitivo con refinamiento | Generador de Tweets impulsado por IA |
| [Parallel](ParallelWorkflow) | Ejecución simultánea de tareas independientes | Estadísticas de Cricket, Evaluación de Ensayos |
| [State Persistence](Persistance) | Mantenimiento del estado a través de ejecuciones del flujo de trabajo | Generador de Chistes con Memoria |
| [Prompt Chaining](PromptChaining) | Encadenamiento de múltiples prompts de LLM | Generador de Entradas de Blog |
| [LLM Integration](LLMWorkflow) | Interacción básica con LLM | Sistema simple de Preguntas y Respuestas |
| [ChatBot](ChatBot) | Interfaz de chat interactiva | ChatBot de IA Full-stack |

## Instalación

1. Clone este repositorio:
   ```bash
   git clone https://github.com/0x-Professor/LangGraph-Practice.git
   cd LangGraph-Practice
   ```

2. Navegue al directorio del flujo de trabajo específico que le interese:
   ```bash
   cd workflow_directory_name
   ```

3. Instale las dependencias requeridas:
   ```bash
   pip install -r requirements.txt
   ```

## Dependencias Comunes

La mayoría de los ejemplos requieren:
- Python 3.8+
- langgraph
- Jupyter Notebook (para ejemplos .ipynb)

Dependencias adicionales para ejemplos específicos:
- langchain-google-genai (para ejemplos de integración de LLM)
- pydantic (para validación de datos)
- fastapi, streamlit (para interfaces web)

## Uso

1. Navegue al directorio del flujo de trabajo específico.
2. Siga las instrucciones en el archivo README.md del flujo de trabajo.
3. Ejecute el ejemplo:
   - Para cuadernos de Jupyter: `jupyter notebook practice.ipynb`
   - Para scripts de Python: `python main.py`

## Contribución

¡Las contribuciones son bienvenidas! No dude en enviar un Pull Request.

1. Haga un fork del repositorio.
2. Cree su rama de característica (`git checkout -b feature/AmazingFeature`).
3. Confirme sus cambios (`git commit -m 'Add some AmazingFeature'`).
4. Haga push a la rama (`git push origin feature/AmazingFeature`).
5. Abra un Pull Request.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT; consulte el archivo [LICENSE](LICENSE) para más detalles.
