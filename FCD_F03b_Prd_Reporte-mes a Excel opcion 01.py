import pandas as pd

# Crea el dataframe de ejemplo
df = pd.DataFrame({'A': ['a', 'a', 'a', 'b', 'b', 'b', 'c', 'c', 'd', 'd'],
                   'B': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                   'C': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})

# Función para insertar filas con subtotal y calcular subtotales
def insertar_fila_subtotal(df):
    """
    Inserta una fila en blanco con "Subtotal" y calcula los subtotales de cada grupo en las columnas numéricas.
    Argumentos:   df (pandas.DataFrame): El dataframe a procesar.
    Devuelve:   pandas.DataFrame: El dataframe con las filas insertadas, subtotales y subtotales calculados.
    """
    # Obtener las columnas numéricas
    columnas_numericas = df.select_dtypes(include='number').columns
    print('Columnas numéricas: ', columnas_numericas)
    print("="*50)

    # Obtener el nombre de la columna de índice
    indice_columna = df.columns.tolist().index(columnas_numericas[0])
    print('Indice de columna: ',indice_columna)
    print("="*50)    
    
    grupo_actual = df.iloc[0, indice_columna - 1]  # Grupo actual (inicialmente el primer valor de la primera columna)
    print('Grupo actual: ',grupo_actual)
    print("="*50)

    subtotales_grupo = {columna: 0 for columna in columnas_numericas}  # Diccionario para almacenar subtotales del grupo actual
    print('Subtotales del grupo: ',subtotales_grupo)
    print("="*50)
    
    rows_to_concat = []  # Lista para almacenar filas a concatenar
    
    for index, fila in df.iterrows():
        if fila.iloc[indice_columna - 1] != grupo_actual:           # Compara el valor actual de la columna de agrupación con la fila anterior
            subtotal = {'A': f"Subtotal {grupo_actual}"}                                              # Crea una fila de subtotal con el nombre del grupo
            subtotal.update({columna: subtotales_grupo[columna] for columna in columnas_numericas})   # Agrega los subtotales del grupo
            rows_to_concat.append(subtotal)                         # Agrega la fila de subtotal a la lista de filas a concatenar
            
            subtotales_grupo = {columna: 0 for columna in columnas_numericas}     # Reinicia los subtotales del grupo actual
            grupo_actual = fila.iloc[indice_columna - 1]                          # Actualiza el grupo actual

        # Actualiza los subtotales del grupo actual
        for columna in columnas_numericas:                    # Itera sobre las columnas numéricas
            subtotales_grupo[columna] += fila[columna]        # Suma el valor de la celda a los subtotales del grupo actual

        rows_to_concat.append(fila)                           # Agrega la fila actual a la lista de filas a concatenar
    
    # Agregar los subtotales del último grupo
    subtotal = {'A': f"Subtotal {grupo_actual}"}              # Crea una fila de subtotal con el nombre del último grupo
    subtotal.update({columna: subtotales_grupo[columna] for columna in columnas_numericas})     # Agrega los subtotales del grupo
    rows_to_concat.append(subtotal)                           # Agrega la fila de subtotal a la lista de filas a concatenar
    
    # Concatena las filas de subtotal al DataFrame original
    df = pd.concat([pd.DataFrame([row]) for row in rows_to_concat], ignore_index=True)
    
    return df

# Aplica la función para insertar filas con subtotal y calcular subtotales
df = insertar_fila_subtotal(df.copy())

# Imprime el dataframe con las filas insertadas, subtotales y subtotales calculados
print(df)
