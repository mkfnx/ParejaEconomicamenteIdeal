import pandas as pd

pob_mayor = 99_747_474
pob_elegible = 43_749_030
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