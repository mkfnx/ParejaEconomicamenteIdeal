import pandas as pd

pob_mayor = 99_747_474
pob_elegible_total = 43_749_030
pob_elegible_hombres = 19_263_700
pob_elegible_mujeres = 24_205_420
salario_minimo_diario = 207.44
salario_minimo_mensual = salario_minimo_diario * 30

dic_opciones_sexo = {'Hombre': 0, 'Mujer': 1, 'Ambos sexos': 2}
dic_opciones_empleo = {'No empleado': 0, 'Empleado': 1, 'Empleados y No empleados': 2}
dic_sueldos = {
    0: 0,
    f'${salario_minimo_mensual:,}': 1,
    f'${salario_minimo_mensual * 2:,}': 2,
    f'${salario_minimo_mensual * 3:,}': 3,
    f'${salario_minimo_mensual * 5:,}': 4,
    f'> ${salario_minimo_mensual * 5:,}': 5
}
rangos_edad = ['15-19', '20-29', '30-39', '40-49', '50-59', '>60']


def abbrev_quantity(quantity):
    if quantity >= 1_000_000:
        return f'{(quantity / 1_000_000):.1f} millones'
    elif quantity >= 1_000:
        return f'{round(quantity / 1_000):.0f} mil'
    else:
        return quantity


def get_rango_edad_str(edad):
    inicio_rango = edad[0].split("-")[0]
    fin_rango = edad[1].split("-")
    if len(fin_rango) == 1:
        fin_rango = fin_rango[0]
    else:
        fin_rango = fin_rango[1]
    return f'{inicio_rango} a {fin_rango}'


def load_data():
    df = pd.read_csv('desglose_ocupacion_inegi.csv')
    df.dropna(axis='index', how='any', inplace=True)
    df.valor = df.valor.astype(int)

    return df


def get_df_for_keys(key_sexo, key_empleo, key_sueldo, key_edad):
    df = load_data()

    return df[
        (df.sexo == key_sexo)
        & (df.empleo == key_empleo)
        & (df.nivel_sueldo >= key_sueldo)
        & (df.rango_edad == key_edad)
        ]


def get_expectations(pop_percentage):
    if pop_percentage < 10:
        expectations_level = 'Desconectado de la realidad :face_with_rolling_eyes:'
        expectations_description = '¿De verdad crees que así encontrarás pareja? :face_with_raised_eyebrow: Necesitas relajarte un poco...'
    elif pop_percentage < 40:
        expectations_level = 'Exigente :flushed:'
        expectations_description = 'Tienes estándares altos. Esperemos que tú también los cumplas  :eyes:'
    elif pop_percentage < 75:
        expectations_level = 'Conformista :face_with_hand_over_mouth:'
        expectations_description = 'Un poco resignado, pero (aún) no desesperado :relieved:'
    else:
        expectations_level = 'Desesperado :grin:'
        expectations_description = 'Estás de plano dispuesto a aceptar cualquier cosa. ¿Quién te hizo tanto daño? :worried:'

    return {
        'level': expectations_level,
        'description': expectations_description
    }


def get_results(key_sexo, pob_filtrada):
    if key_sexo == 0:
        sexo_seleccionado = 'hombres'
        porcentaje_pob = pob_filtrada / pob_elegible_hombres * 100
        pob_elegible = pob_elegible_hombres
    elif key_sexo == 1:
        sexo_seleccionado = 'mujeres'
        porcentaje_pob = pob_filtrada / pob_elegible_mujeres * 100
        pob_elegible = pob_elegible_mujeres
    else:
        sexo_seleccionado = 'personas'
        porcentaje_pob = pob_filtrada / pob_elegible_total * 100
        pob_elegible = pob_elegible_total

    return {
        'sexo_seleccionado': sexo_seleccionado,
        'porcentaje_pob': porcentaje_pob,
        'pob_elegible': pob_elegible,
    }
