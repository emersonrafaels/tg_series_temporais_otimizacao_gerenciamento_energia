from pathlib import Path
from inspect import stack

import streamlit as st
from loguru import logger

from src.config_app.config_app import settings
from src.utils.pandas_functions import load_data
from src.utils.dataframe_explorer import dataframe_explorer
from src.app_pages import datasets_ghcn, datasets_inmet

# DEFININDO O DIRETÓRIO ROOT
dir_root = Path(__file__).absolute().parent.parent.parent


def convert_dataframe_explorer(data, style):
    """

    CONVERTENDO O DATAFRAME PARA UMA VERSÃO EXPLORÁVEL

    # Arguments
            data                   - Required: Dados para plotar (DataFrame)
            style				   - Required: Estilo do dataframe (String)

    # Returns
            style				   - Required: Estilo do dataframe (String)
            dataframe_explorer     - Required: Dataframe formato explorer (Object)

    """

    if style == "dataframe_explorer":
        return style, dataframe_explorer(data, case=False)

    else:
        logger.warning("OPÇÃO NÃO VÁLIDA - {}".format(stack()[0][3]))

    return style, None


def load_datasets():
    # OBTENDO A LISTA DE DATASETS DISPONÍVEIS O SELECT BOX DE DATASETS
    st.session_state["list_datasets"] = settings.get("LIST_DATASETS")

    # CRIANDO O MARKDOWN DE TÍTULO
    st.markdown(
        "# {}".format(settings.get("APPNAME_TITLE", "TG UFABC - ENERGIA - PREVISORES"))
    )

    st.markdown("# 1. Selecione o conjunto de dados climáticos")

    # CRIANDO O SELECT BOX DE DATASETS
    st.session_state["list_datasets"] = settings.get("LIST_DATASETS")

    st.session_state["filter_dataset"] = st.selectbox(
        label="Conjunto de dados",
        options=st.session_state["list_datasets"],
    )

    if st.session_state["filter_dataset"] == "GHCN":
        dir_measurements = settings.get("DATA_DIR_STATIONS_GHCN")
    elif st.session_state["filter_dataset"] == "INMET":
        dir_measurements = settings.get("DATA_DIR_STATIONS_INMET")

    if dir_measurements:
        # OBTENDO OS DADOS DE ESTAÇÕES METEOROLÓGICAS
        dir_measurements = settings.get("DATA_DIR_STATIONS_GHCN")
        data = load_data(str(Path(dir_root, dir_measurements)))

        logger.info("DADOS OBTIDOS COM SUCESSO")

        # SALVANDO O DATASET
        st.session_state["dataset"] = data.get("DATAFRAME_RESULT")

        st.markdown("# 2. Dados do conjunto")

        # OBTENDO O DATAFRAME
        dataframe_explorer_type, dataframe_return = convert_dataframe_explorer(
            data=st.session_state["dataset"],
            style=settings.get("OPTION_DATAFRAME_EXPLORER", "dataframe_explorer"),
        )

        if st.session_state["filter_dataset"] == "GHCN":
            # CARREGANDO OS DADOS DO GHCN
            datasets_ghcn.load_dataset_ghcn(dataframe_return=dataframe_return)

        elif st.session_state["filter_dataset"] == "INMET":
            # CARREGANDO OS DADOS DO INMET
            datasets_inmet.load_dataset_inmet(dataframe_return=dataframe_return)

    else:
        logger.error("OPÇÃO NÃO VÁLIDA")
