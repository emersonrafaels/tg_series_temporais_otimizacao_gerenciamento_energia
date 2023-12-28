import numpy as np
import pandas as pd
import streamlit as st
from loguru import logger

from src.utils.config_dataframe_explorer import (
    COLUMN_CONFIG_DATASET_INMET,
)
from src.utils.map.map_functions import folium_static
from src.config_app.config_app import settings
from src.utils.graphs.graphs_datasets import create_graph_timeseries_datasets
from src.utils.graphs.time_series_analysis import plot_mean_variance_over_time
from src.utils.statistics_functions import (
    get_difference_list_values_versus_global_value,
)
from src.utils.map.map_app import plot_map_dataset_ghcn


def load_dataset_inmet(dataframe_return):
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
    column_timeseries_x_axis = settings.get("COLUMN_TIMESERIES_X_AXIS_INMET", "")

    # TEMPERATURA
    column_timeseries_temp_axis = settings.get("COLUMN_TIMESERIES_TEMP_INMET", "")
