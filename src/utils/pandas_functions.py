import streamlit as st
import pandas as pd


def column_to_uppercase(data):
    # OBTENDO TODAS AS COLNAS DO DATAFRAME
    # APLICANDO UPPERCASE
    newcols = [column.upper() for column in data.columns]

    # FORMATANDO O DATAFRAME
    data.columns = newcols

    # RETORNANDO O DATAFRAME FORMATADO EM UPPERCASE
    return data


def rows_to_uppercase(data, trim=False):
    # OBTENDO TODAS AS COLNAS DO DATAFRAME
    # APLICANDO UPPERCASE
    for column in data.select_dtypes(include="O").columns:
        if trim:
            data[column] = data[column].apply(lambda x: str(x).upper().strip())
        else:
            data[column] = data[column].apply(lambda x: str(x).upper())

    return data


def select_columns_dataframe(data, list_columns_to_select):

    """

        SELECIONA AS COLUNAS DESEJADAS
        DE UM DATAFRAME

        ANTES DE REALIZAR A SELEÇÃO
        REALIZA OS FILTROS DESEJADOS.

        # Arguments
            data                          - Required: Dados para filtrar (DataFrame)
            list_columns_to_select        - Required: Lista de colunas
                                                      para filtrar (List)

        # Returns
            result_data                   - Required: Dados após filtro (DataFrame)

    """

    list_columns_result = []

    for value in list_columns_to_select:
        if value in data.columns and value not in list_columns_result:
            list_columns_result.append(value)

    # FILTRANDO COLUNAS DESEJADAS
    result_data = data[list_columns_result]

    return result_data


@st.cache_data
def load_data(
    data_dir,
    header=0,
    separator=",",
    column_uppercase=False,
    row_uppercase=False,
    trim_values=True,
    multiindex=False,
):
    """

    REALIZA A LEITURA DOS DADOS

    # Arguments
        data_dir                 - Required: Dado a ser lido (Path)
        header                   - Optional: Linha inicial dos dados (Integer)
        separator                - Optional: Para arquivos csv, identifica o
                                             separador dos dados (String)
        column_uppercase         - Optional: Validador para tornar
                                             todas colunas uppercase (Boolean)
        row_uppercase            - Optional: Validador para tornar
                                             todas linhas (valores) uppercase (Boolean)
        trim_values              - Optional: Validador para remover espaços antes e depois,
                                             em valores strings (Boolean)
        multiindex               - Optional: Se é desejado ler um dataframe multiindex (Boolean)

    # Returns
        df                       - Required: Dado após leitura (DataFrame)

    """

    # INICIANDO O DICT RESULT
    dict_result = {}

    # REALIZANDO A LEITURA DOS DADOS
    if "csv" in data_dir:
        df = pd.read_csv(data_dir, header=header, sep=separator)
    else:
        df = pd.read_excel(data_dir, header=header)

    if not multiindex:
        if column_uppercase:
            df = column_to_uppercase(data=df)
        if row_uppercase:
            df = rows_to_uppercase(data=df, trim=trim_values)

    if multiindex:
        df_columns = df.columns.to_numpy()
        df_columns_level0 = df.columns.get_level_values(0)
        df_columns_level1 = df.columns.get_level_values(1)

        df.columns = df_columns_level1

        dict_result["DF_COLUMNS"] = df_columns
        dict_result["DF_COLUMNS_LEVEL0"] = df_columns_level0
        dict_result["DF_COLUMNS_LEVEL1"] = df_columns_level1

        if column_uppercase:
            df = column_to_uppercase(data=df)
        if row_uppercase:
            df = rows_to_uppercase(data=df, trim=trim_values)

    dict_result["DATAFRAME_RESULT"] = df

    return dict_result
