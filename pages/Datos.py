import streamlit as st
from helpers import load_data

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

st.title('Sobre los datos')

st.markdown("""
* Información de INEGI México  
\"Encuesta Nacional de Ocupación y Empleo (ENOE), población de 15 años y más de edad.\"  
Primer trimestre 2023  
[https://www.inegi.org.mx/programas/enoe/15ymas/#Tabulados](https://www.inegi.org.mx/programas/enoe/15ymas/#Tabulados)
""")

st.markdown("""
Los datos y el código de este proyecto están [disponibles en GitHub](https://github.com/mkfnx)
""")

st.markdown("""
La información fue recopilada realizando consultas a la dirección web del INEGI que se indica arriba.  

A partir de dichas consultas se elaboró la tabla que se muestra abajo,
la cual está compuesta por las combinaciones posibles de los criterios de selección
(sexo, situación laboral, rango de sueldo y rango de edad)
y que en cada fila contiene el valor de la población que cumple con los criterios correspondientes.
""")

df = load_data()
st.write(df)
st.download_button(
    label='Descargar datos en CSV',
    data=convert_df(df),
    file_name='datos_pareja_economica_ideal_mkfnx.csv',
    mime='text/csv',
    key=None
)

st.markdown("""
Algunos de los  valores para los criterios de selección se sustituyeron por números
para facilitar la captura de información, y son los siguientes:
* sexo
  * 0: Hombre
  * 1: Mujer
  * 2: Ambos
* empleo:
  * 0: Sin empleo
  * 2: Con Empleo
  * 3: Ambos
* nivel_sueldo:
  * 0: Sin ingresos
  * 1: Hasta 1 salario mínimo
  * 2: De 1 a 2 salarios mínimos
  * 3: De 2 a 3 salarios mínimos
  * 4: De 3 a 5 salarios mínimos
  * 5: Más de 5 salarios mínimos
""")

st.divider()

st.text('Creado por Miguel López (@mkfnx)')
st.markdown('Más de mi contenido y proyectos en [https://beacons.ai/mkfnx](https://beacons.ai/mkfnx)')
st.markdown('Política de privacidad: [https://mkfnx.github.io/apps-privacy-policy-es]('
            'https://mkfnx.github.io/apps-privacy-policy-es)')
