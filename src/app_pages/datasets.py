import os
from pathlib import Path
from inspect import stack

import pandas as pd
import streamlit as st
from loguru import logger

from config_app.config_app import settings
from utils.map.map_functions import folium_static
from utils.pandas_functions import load_data
from utils.dataframe_explorer import dataframe_explorer
from utils.config_dataframe_explorer import (
    COLUMN_CONFIG_DATASET_GHCN,
    COLUMN_CONFIG_DATASET_INMET,
)
from utils.graphs.graphs_datasets import create_graph_timeseries_datasets
from utils.map.map_app import plot_map_dataset_ghcn

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

    st.markdown("# 1. Conjuntos de dados - Dados climáticos")

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
            # OBTENDO A CONFIG DAS COLUNAS
            COLUMN_CONFIG = COLUMN_CONFIG_DATASET_GHCN

            # OBTENDO SE HÁ ORDEM DAS COLUNAS
            list_columns_order = settings.get(
                "LIST_COLUMNS_ORDER_GHCN", dataframe_return.columns
            )

            # FILTRANDO O DATAFRAME
            dataframe_return = dataframe_return[list(list_columns_order)]

            # OBTENDO A LISTA DE AGRUPAMENTOS PARA ESSE DATASET
            st.session_state["list_filter_dataset_group"] = settings.get(
                "LIST_COLUMNS_GROUP_GHCN", dataframe_return.columns
            )

            # OBTENDO AS COLUNAS PARA PLOT
            column_timeseries_x_axis = settings.get(
                "COLUMN_TIMESERIES_X_AXIS_GHCN", "measurement date"
            )

            column_timeseries_temp_axis = settings.get(
                "COLUMN_TIMESERIES_TEMP_GHCN", "avg_temp"
            )

        elif st.session_state["filter_dataset"] == "INMET":
            # OBTENDO A CONFIG DAS COLUNAS
            COLUMN_CONFIG = COLUMN_CONFIG_DATASET_INMET

            # OBTENDO SE HÁ ORDEM DAS COLUNAS
            list_columns_order = settings.get(
                "LIST_COLUMNS_ORDER_INMET", dataframe_return.columns
            )

            # FILTRANDO O DATAFRAME
            dataframe_return = dataframe_return[list(list_columns_order)]

            # OBTENDO A LISTA DE AGRUPAMENTOS PARA ESSE DATASET
            st.session_state["list_filter_dataset_group"] = settings.get(
                "LIST_COLUMNS_GROUP_INMET", dataframe_return.columns
            )

            # OBTENDO AS COLUNAS PARA PLOT
            column_timeseries_x_axis = settings.get(
                "COLUMN_TIMESERIES_X_AXIS_INMET", ""
            )

            column_timeseries_temp_axis = settings.get(
                "COLUMN_TIMESERIES_TEMP_INMET", ""
            )

        # INCLUINDO O DATAFRAME
        selected_df = st.dataframe(
            dataframe_return,
            use_container_width=True,
            column_config=COLUMN_CONFIG,
            hide_index=True,
        )

        # OBTENDO O DATAFRAME DAS LINHAS SELECIONADAS
        st.session_state["selected_df"] = dataframe_return

        # QUANTIDADE DE DADOS SELECIONADOS
        st.text(
            "Quantidade de medições: {}".format(len(st.session_state["selected_df"]))
        )

        st.markdown("# 3. Distribuição das estações metereológicas")
        st.text(
            "- No mapa estarão as estações metereológicas após os filtros aplicados no conjunto acima"
        )
        st.text(
            "- Utilize o zoom lateral, ou o zoom do mouse, para visualizar mais detalhes dos clusters de agências"
        )

        # PLOTANDO O MAPA DAS ESTAÇÕES METEREOLÓGICAS
        validator_map, st.session_state["mapobj"], _ = plot_map_dataset_ghcn(
            data=st.session_state["selected_df"]
        )

        st_data = folium_static(
            st.session_state["mapobj"],
            width=900,
            height=500,
            add_categorical_legend=False,
        )

        st.markdown("# 4. Séries temporais medidas no conjunto de dados")

        if st.session_state["filter_dataset"] == "GHCN":
            # SELECIONAR TIPO DE AGRUPAMENTO
            st.session_state["filter_dataset_group"] = st.selectbox(
                label="Selecione o modo de agrupamento",
                options=st.session_state["list_filter_dataset_group"],
            )

            # DEFININDO QUE O GROUPBY SERÁ PELA COLUNA ESCOLHA + A COLUNA PADRÃO
            filter_groupby = [st.session_state["filter_dataset_group"]] + [
                column_timeseries_x_axis
            ]

            # DEFININDO AS OPÇÕES PARA O FILTRO MULTISELECT DO GROUP
            options_group = st.session_state["selected_df"][st.session_state["filter_dataset_group"]].sort_values().unique()

            # CRIANDO MULTISELECGT BASEADO NO FILTRO
            # SELECIONAR TIPO DE AGRUPAMENTO
            filter_groupby_value = st.multiselect(
                label="Selecione os valores para exibir",
                options=options_group,
                default=options_group[0],
            )

            # FILTRANDO BASEADO NO MULTISELECT
            dataframe_plot = st.session_state["selected_df"][st.session_state["selected_df"][st.session_state["filter_dataset_group"]].isin(filter_groupby_value)]

            # REALIZANDO O PLOT DAS SÉRIES TEMPORAIS
            fig = create_graph_timeseries_datasets(
                data=dataframe_plot,
                groupby_column=filter_groupby,
                column_x_axis=column_timeseries_x_axis,
                column_y_axis=column_timeseries_temp_axis,
                fig_title="Time Series - Temperatura",
            )

            st.plotly_chart(figure_or_data=fig,
                            use_container_width=True)

    else:
        logger.error("OPÇÃO NÃO VÁLIDA")
