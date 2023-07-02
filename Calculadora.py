import streamlit as st
from helpers import *

st.title('Probabilidad de encontrar tu pareja (económicamente) ideal en México')
st.markdown("""
1. Selecciona las características que buscas en tu pareja.
2. Obtén el porcentaje de personas que cumplen con tus preferencias.
""")

st.divider()

st.header('Selecciona las características que buscas en tu pareja')

# Sexo
st.subheader('Sexo')
sexo = st.radio('Selección de sexo de la pareja', tuple(dic_opciones_sexo), label_visibility='collapsed', horizontal=True)
key_sexo = dic_opciones_sexo[sexo]

# Empleo
st.subheader('Situación laboral')
empleo = st.radio('Selección de situación laboral de la pareja', tuple(dic_opciones_empleo), label_visibility='collapsed', horizontal=True)
key_empleo = dic_opciones_empleo[empleo]

# Sueldo
key_sueldo = -1
sueldo = None
if key_empleo > 0:
    st.subheader('Mínimo de sueldo que deseas que perciba tu pareja')
    st.text(f'Rangos en salarios mínimos mensuales (${salario_minimo_diario} x 30 días).')
    sueldo = st.select_slider('Mínimo de sueldo', dic_sueldos)
    key_sueldo = dic_sueldos[sueldo]
key_sueldo = 0 if key_sueldo == -1 else key_sueldo

# Edad
st.subheader('Edad')
st.text('La edad en la fuente de datos está reportada en rangos.')
st.text('El rango para el cálculo se forma con el valor menor izquierdo y el mayor derecho')
edad = st.select_slider('Selecciona el rango de edad', rangos_edad, (rangos_edad[0], rangos_edad[-1]))
key_edad = ' | '.join(edad)
rango_edad = get_rango_edad_str(edad)
st.text(f'Rango seleccionado: {rango_edad} años')

st.divider()

# Resultados
df_resultados = get_df_for_keys(key_sexo, key_empleo, key_sueldo, key_edad)
pob_filtrada = df_resultados.valor.sum()
porcentaje_pob = pob_filtrada / pob_elegible * 100
sueldo_str = f'* Mínimo \\{sueldo} pesos al mes' if sueldo else ''
if porcentaje_pob < 25:
    situacion = 'Desconectado de la realidad'
    desc_situacion = '¿De verdad crees que así encontrarás pareja? Necesitas relajarte un poco...'
elif porcentaje_pob < 50:
    situacion = 'Exigente'
    desc_situacion = 'Tienes estándares altos. Ojalá tú también los cumplas'
elif porcentaje_pob < 75:
    situacion = 'Conformista'
    desc_situacion = 'Un poco resignado, pero (aún) no desesperado'
else:
    situacion = 'Desesperado'
    desc_situacion = 'Estás de plano dispuesto a aceptar cualquier cosa. ¿Quién te hizo tanto daño?'
st.title('Tu probabilidad de encontrar la pareja ideal es:')
st.title(f'{porcentaje_pob:.2f}%')
st.text(f'(Porcentaje de población que cumple las características seleccionadas)')
st.markdown(f"""
* {sexo}
* {empleo}
{sueldo_str}
* {rango_edad} años
""")
st.markdown(f'es decir, {abbrev_quantity(pob_filtrada)} de {abbrev_quantity(pob_elegible)} personas')
st.subheader(f'Tu situación es:')
st.title(situacion)
st.markdown(f'##### {desc_situacion}')

st.divider()

st.subheader(f'La población inicial es: {abbrev_quantity(pob_elegible)} de personas')
st.markdown("""
Este número incluye personas con estas características:
- Ambos sexos
- Actualmente solteros (incluyendo "alguna vez unidos")
- Al menos 15 años (edad más baja para ser considerado en los datos)
""")

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
