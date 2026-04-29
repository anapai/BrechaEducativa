# BrechaEducativa
Brecha educativa en México: ¿Cómo varía el acceso a la educación entre los estados de México?                                                                 
Existen diferencias significativas en el acceso a la educación entre los estados de México, reflejadas en la matrícula y cobertura educativa. 

Brecha educativa en México: Público vs Privado

Pregunta de investigación

¿Cómo se distribuye la matrícula entre educación pública y privada en México y cómo varía esta diferencia según el estado, el nivel educativo y el tiempo?

Objetivo del proyecto

Construir una narrativa visual interactiva que permita analizar la brecha entre educación pública y privada en México, utilizando datos reales de la SEP y visualizaciones dinámicas que faciliten la interpretación de tendencias nacionales y regionales.

Fuente de datos

Los datos utilizados provienen de la Secretaría de Educación Pública (SEP), específicamente de la serie histórica de matrícula por entidad federativa.

Archivo utilizado:

* serie_historica_entidades_sep.csv

Fuente oficial:
https://www.planeacion.sep.gob.mx/estadisticaeducativas.aspx

También se utilizó un archivo geográfico en formato GeoJSON para la visualización del mapa:

* states_full.geojson 

Proceso de preparación de datos

El desarrollo del proyecto siguió varias etapas:

1. Descarga de datos
   Se descargó la base de datos oficial de la SEP en formato CSV con información histórica de matrícula por estado, sector y tipo.


2. Limpieza inicial en Excel
   Antes de trabajar en Python, se realizó un preprocesamiento en Excel para facilitar el análisis:

* Eliminación de columnas innecesarias
* Revisión de estructura de la base
* Verificación de nombres de columnas
* Asegurar consistencia en categorías

3. Limpieza y transformación en Python (Pandas)

Posteriormente, se trabajó con Pandas para estructurar correctamente los datos:

* Eliminación de espacios en nombres de columnas
* Transformación de formato ancho a formato largo (melt)
* Estandarización de valores en la columna Tipo:

  * PUBLICO
  * PRIVADO
* Eliminación de caracteres (comas) en la matrícula
* Conversión de la matrícula a valores numéricos
* Conversión del año a tipo entero
* Filtrado para trabajar únicamente con datos de educación pública y privada

Desarrollo de visualizaciones

Etapa 1: Exploración con Matplotlib

Inicialmente se desarrollaron gráficas estáticas utilizando Matplotlib para validar el comportamiento de los datos:

1. Evolución de matrícula en el tiempo
2. Comparación por nivel educativo
3. Brecha por estado

Estas visualizaciones permitieron:

* Validar la limpieza de datos
* Identificar patrones iniciales
* Definir el enfoque del análisis

Etapa 2: Visualizaciones interactivas

Posteriormente, se migró a un entorno interactivo utilizando:

* Plotly para gráficas dinámicas
* Shiny para Python para crear una aplicación web interactiva

Visualizaciones finales

La aplicación incluye las siguientes gráficas:

1. Matrícula pública vs privada en el tiempo
   Permite observar la evolución nacional y comparar tendencias entre ambos sectores.

2. Matrícula por nivel educativo
   Muestra cómo se distribuye la matrícula en distintos niveles educativos y cómo cambia la participación pública vs privada.

3. Estados con mayor brecha
   Identifica los estados donde existe mayor diferencia entre matrícula pública y privada.

4. Mapa de México (brecha educativa)
   Visualización geográfica que permite analizar la distribución de la brecha por entidad federativa.

Interactividad

La aplicación incluye filtros dinámicos:

* Estado
* Nivel educativo
* Año

Las gráficas se actualizan automáticamente según los filtros seleccionados, permitiendo un análisis exploratorio completo.

Diseño

Se implementó una interfaz moderna con:

* Tema oscuro
* Paleta de colores inspirada en diseño institucional
* Contenedores visuales organizados
* Experiencia tipo dashboard con narrativa

Tecnologías utilizadas

* Python
* Pandas
* Plotly
* Shiny para Python
* GeoJSON (mapa)
* Matplotlib (fase exploratoria)

Cómo ejecutar el proyecto

1. Clonar el repositorio:

git clone <URL_DEL_REPOSITORIO>

2. Crear entorno virtual:

python -m venv .venv

3. Activar entorno:

.venv\Scripts\activate

4. Instalar dependencias:

pip install -r requirements.txt

5. Ejecutar la aplicación:

python -m shiny run --reload BrechaEducativa/app/app.py

Principales hallazgos

* La educación pública concentra la mayor parte de la matrícula en México
* La participación de la educación privada varía según el nivel educativo
* Existen diferencias importantes entre estados en la brecha educativa
* La brecha público-privada cambia con el tiempo y el contexto regional

Aplicación en línea
https://r8tr6j-ana0pau.shinyapps.io/brechaeducativa/


Referencias:
*https://shiny.posit.co/py/get-started/debug.html
*https://www.planeacion.sep.gob.mx/estadisticaeducativas.aspx
*https://www.ex-presate.com.mx/el-poder-del-storytelling-visual-como-contar-historias-a-traves-del-diseno-grafico/
