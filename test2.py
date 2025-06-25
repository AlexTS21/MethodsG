import pandas as pd

ruta_entrada = 'COVID19MEXICO2021.csv'
ruta_salida = 'pueblaGob.csv'

def procesar_csv(ruta_entrada, ruta_salida):
    # Columnas requeridas
    columnas_objetivo = [
        'SEXO', 'NACIONALIDAD', 'ENTIDAD_RES', 'INTUBADO', 'NEUMONIA', 'EDAD',
        'EMBARAZO', 'INDIGENA', 'DIABETES', 'EPOC', 'ASMA', 'INMUSUPR',
        'HIPERTENSION', 'CARDIOVASCULAR', 'OBESIDAD', 'RENAL_CRONICA',
        'TABAQUISMO', 'TOMA_MUESTRA_ANTIGENO', 'CLASIFICACION_FINAL'
    ]

    # Leer solo las columnas necesarias
    df = pd.read_csv(ruta_entrada)
    print("Filas cargadas:", len(df))

    # Filtrar por NACIONALIDAD = 1, ENTIDAD_RES = 21 y CLASIFICACION_FINAL en [1, 2, 7]
    df = df[
        (df['NACIONALIDAD'] == 1) &
        (df['ENTIDAD_RES'] == 21) &
        (df['CLASIFICACION_FINAL'].isin([1, 2, 7]))
    ]

    # Mantener solo valores 1 o 2 en columnas binarias (excepto EDAD y CLASIFICACION_FINAL)
    columnas_binarias = [col for col in columnas_objetivo if col not in ['EDAD', 'NACIONALIDAD', 'ENTIDAD_RES', 'CLASIFICACION_FINAL']]
    for col in columnas_binarias:
        df = df[df[col].isin([1, 2])]
        df[col] = df[col].replace(2, 0)

    # Transformar CLASIFICACION_FINAL → class
    df['class'] = df['CLASIFICACION_FINAL'].replace({1: 1, 2: 1, 7: 0})
    df = df.drop(columns=['CLASIFICACION_FINAL'])

    # Resetear índice y agregar columna "id"
    df.reset_index(drop=True, inplace=True)
    df.insert(0, 'id', df.index)

    # Seleccionar solo las columnas deseadas + id + class
    columnas_finales = ['id'] + [col for col in columnas_objetivo if col != 'CLASIFICACION_FINAL'] + ['class']
    df = df[columnas_finales]

    # Guardar el nuevo archivo
    df.to_csv(ruta_salida, index=False)

# Ejecutar la función
procesar_csv(ruta_entrada=ruta_entrada, ruta_salida=ruta_salida)
