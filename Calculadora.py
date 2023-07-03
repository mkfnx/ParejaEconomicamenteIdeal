import streamlit as st
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')
from pywaffle import Waffle
from helpers import *

st.set_page_config(
    page_title='Calculadora de Pareja (Económicamente) Ideal - @mkfnx',
)

st.title('Probabilidad de encontrar tu pareja (económicamente) ideal en México')
st.markdown("""
Instrucciones:  
1. Selecciona las características que buscas en tu pareja.
2. Obtén el porcentaje de personas que cumplen con tus preferencias.
""")

st.divider()

st.header('Selecciona las características que buscas en tu pareja')

# Sexo
st.subheader('Sexo')
sexo = st.radio('Selección de sexo de la pareja', tuple(dic_opciones_sexo), label_visibility='collapsed',
                horizontal=True)
key_sexo = dic_opciones_sexo[sexo]

# Empleo
st.subheader('Situación laboral')
empleo = st.radio('Selección de situación laboral de la pareja', tuple(dic_opciones_empleo),
                  label_visibility='collapsed', horizontal=True)
key_empleo = dic_opciones_empleo[empleo]

# Sueldo
key_sueldo = -1
sueldo = None
st.subheader('Mínimo de sueldo que deseas que perciba tu pareja')
if key_empleo > 0:
    st.markdown(f'Rangos en salarios mínimos mensuales (${salario_minimo_diario} x 30 días).')
else:
    st.markdown('El rango de sueldo no está habilitado si seleccionaste "No empleado" en Situación Laboral.')
sueldo = st.select_slider('Mínimo de sueldo', dic_sueldos, disabled=(key_empleo == 0))
key_sueldo = dic_sueldos[sueldo]
key_sueldo = 0 if key_sueldo == -1 else key_sueldo

# Edad
st.subheader('Edad')
st.markdown('La edad en la fuente de datos está reportada en rangos, con un mínimo de 15 años.')
st.markdown('El rango para el cálculo se forma con el valor menor izquierdo y el mayor derecho.')
edad = st.select_slider('Selecciona el rango de edad', rangos_edad, (rangos_edad[0], rangos_edad[-1]))
key_edad = ' | '.join(edad)
rango_edad = get_rango_edad_str(edad)
st.markdown(f'Rango seleccionado: {rango_edad} años')

st.divider()

# Resultados
df_resultados = get_df_for_keys(key_sexo, key_empleo, key_sueldo, key_edad)
pob_filtrada = df_resultados.valor.sum()
sueldo_str = f'* Mínimo \\{sueldo} pesos al mes' if sueldo else ''
resultados = get_results(key_sexo, pob_filtrada)
porcentaje_pob = resultados['porcentaje_pob']
sexo_seleccionado = resultados['sexo_seleccionado']
pob_elegible = resultados['pob_elegible']
expectations = get_expectations(porcentaje_pob)

st.title('Resultados:')

# Expectations judgement
st.subheader(f'Tus expectativas son:')
st.title(expectations['level'])
st.markdown(f'##### {expectations["description"]}')

st.title(f'{porcentaje_pob:.2f}%')
st.markdown(f'de {sexo_seleccionado} cumplen las características que indicaste')

# Waffle chart
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=20,
    values=[round(porcentaje_pob), 100 - round(porcentaje_pob)],
    labels=['Cumplen', 'No cumplen'],
    colors=['#F54B4B', '#B2B2B2'],
)
st.pyplot(fig)

st.markdown(f"""
* {sexo}
* {empleo}
{sueldo_str}
* {rango_edad} años
""")
st.markdown(f'es decir, {abbrev_quantity(pob_filtrada)} de {abbrev_quantity(pob_elegible)} {sexo_seleccionado}.')

# Población max
st.divider()

st.subheader(f'La población inicial es: {abbrev_quantity(pob_elegible_total)} de personas')
st.markdown("""
Este número incluye personas con estas características:
- Ambos sexos
- Actualmente solteros (incluyendo "alguna vez unidos")
- Al menos 15 años (edad más baja para ser considerado en los datos)
""")

# Footer
st.divider()

st.markdown("""
* Información de INEGI México  
\"Encuesta Nacional de Ocupación y Empleo (ENOE), población de 15 años y más de edad.\"  
Primer trimestre 2023  
[https://www.inegi.org.mx/programas/enoe/15ymas/#Tabulados](https://www.inegi.org.mx/programas/enoe/15ymas/#Tabulados)
""")

st.markdown('* Creado por Miguel López (@mkfnx)')
st.markdown('Más de mi contenido y proyectos en [https://beacons.ai/mkfnx](https://beacons.ai/mkfnx)')
st.markdown('Política de privacidad: [https://mkfnx.github.io/apps-privacy-policy-es]('
            'https://mkfnx.github.io/apps-privacy-policy-es)')
