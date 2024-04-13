import pandas as pd

# Función para cargar datos desde un archivo CSV
def load_data():
    return pd.read_csv('netflix1.csv')

# Función para mostrar información básica del DataFrame
def display_data_info(df):
    print(df)
    print(df.info())

# Función para verificar duplicados en el DataFrame
def check_duplicates(df):
    duplicated_rows = df[df.duplicated(keep=False)]
    if not duplicated_rows.empty:
        print("Filas duplicadas en el DataFrame:")
        print(duplicated_rows)
    else:
        print("No hay filas duplicadas en el DataFrame.")

# Función para mostrar los valores más repetidos en cada columna
def values_count(df, top_n=40):
    for column in df.columns:
        values_repet = df[column].value_counts().head(top_n)
        print(f"\nTop {top_n} valores más repetidos en la columna '{column}':")
        print(values_repet)

# Función para contar columnas con "Not Given"
def count_not_given(df):
    is_not_given = df.apply(lambda x: x == 'Not Given')
    columns_with_not_given = is_not_given.sum()
    return columns_with_not_given[columns_with_not_given > 0]

# Limpieza de los datos y procesamiento de los datos
def data_treatment():
    # Cargar datos y eliminar la primera columna
    df_t = load_data().drop(df.columns[0], axis=1)
    # Cambiar el nombre de las columnas
    new_column_names = ['Type', 'Title', 'Director', 'Country', 'Date_Added', 'Release_Year', 'Clasificacion', 'Duration', 'Category']
    df_t.columns = new_column_names
    # Separar y convertir las columnas 'Date_Added' en 'Month_Added', 'Day_Added', 'Year_Added'
    df_t[['Month_Added', 'Day_Added', 'Year_Added']] = df_t['Date_Added'].str.split('/', expand=True)
    df_t[['Month_Added', 'Day_Added', 'Year_Added']] = df_t[['Month_Added', 'Day_Added', 'Year_Added']].apply(pd.to_numeric, errors='coerce')
    # Eliminar la columna 'Date_Added'
    df_t = df_t.drop('Date_Added', axis=1)
    # Dividir la columna 'Category' en varias columnas
    df_category_split = df_t['Category'].str.split(', ', expand=True)
    # Agregar las nuevas columnas al DataFrame original con nombres específicos
    for i in range(df_category_split.shape[1]):
        new_column_name = f'Category_{i + 1}'
        df_t[new_column_name] = df_category_split[i]
    # Reemplazar los valores None con "False" en todo el DataFrame
    df_t.replace(to_replace=[None], value="False", inplace=True)
    # Eliminar la columna 'Category'
    df_t = df_t.drop('Category', axis=1)
    # Obtener el nombre de las columnas
    column_names = df_t.columns.tolist()
    # Mover la columna 'Type' después de 'Duration'
    column_names.remove('Type')
    column_names.insert(column_names.index('Duration') + 1, 'Type')
    # Reorganizar el DataFrame con las nuevas posiciones de las columnas y eliminar duplicados
    return df_t[column_names].drop_duplicates()

if __name__ == "__main__":
    df = load_data()
    df_t = data_treatment()

    # Verificar duplicados
    print("************************************************************************************************************"+
          "\n************************************************************************************************************"+
          "\n************************************Verificacion de duplicidad en ambos*************************************"+
          "\n************************************************************************************************************"+
          "\n************************************************************************************************************")
    print("Duplicados en df original...")
    check_duplicates(df=df.drop(df.columns[0], axis=1))
    print("\n")
    print("Duplicados en df a procesar...")
    check_duplicates(df_t)

    # Muestra los 40 valores más repetidos en cada columna
    print("************************************************************************************************************"+
        "\n************************************************************************************************************"+
        "\n************************************Verificacion del top 40 de valores**************************************"+
        "\n************************************************************************************************************"+
        "\n************************************************************************************************************")
    values_count(df_t, 40)

    # Contar y mostrar columnas con "Not Given"
    print("************************************************************************************************************"+
        "\n************************************************************************************************************"+
        "\n************************************Verificacion cantida de Not Given***************************************"+
        "\n************************************************************************************************************"+
        "\n************************************************************************************************************")
    not_given_columns = count_not_given(df_t)
    print("Columnas con 'Not Given':")
    print(not_given_columns)

    # Visualizar información
    print("************************************************************************************************************"+
          "\n************************************************************************************************************"+
          "\n************************************Información del DataFrame Original**************************************"+
          "\n************************************************************************************************************"+
          "\n************************************************************************************************************")
    display_data_info(df)
    print("************************************************************************************************************"+
          "\n************************************************************************************************************"+
          "\n************************************Información del DataFrame a Procesar************************************"+
          "\n************************************************************************************************************"+
          "\n************************************************************************************************************")
    display_data_info(df_t)

    # Guardar el DataFrame limpio en un nuevo archivo CSV
    df_t.to_csv('netflix_cleaned.csv', index=False)

