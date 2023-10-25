import os
from pathlib import Path

import pandas as pd

try:
    from src.config_app.config_app import settings
    from src.utils.map.map_functions import load_map
except ModuleNotFoundError:
    from config_app.config_app import settings
    from utils.map.map_functions import load_map


def plot_map_dataset_ghcn(data):
    """

    PLOTANDO O MAPA DO DATASET GHCN

    # Arguments
            data               - Required: Dados das estações para
                                                                       plotar no mapa (DataFrame)

    # Returns

    """

    # TORNANDO OS DADOS NULOS EM "-", PARA MELHOR VISUALIZAÇÃO
    data = data.fillna("-")

    # FILTRANDO E ORDENANDO AS COLUNAS COMO DESEJADAS
    data = data[list(settings.get("LIST_COLUMNS_ORDER_MAP_GHCN"))]

    # REMOVENDO DUPLICIDADES
    data = data.drop_duplicates()

    # PLOTANDO O MAPA
    validator, mapobj, _ = load_map(
        data=data,
        map_layer_default=settings.get("MAP_LAYER_DEFAULT", "openstreetmap"),
        circle_radius=0,
        validator_add_layer=settings.get("VALIDATOR_ADD_LAYER", False),
        column_status=settings.get("COLUMN_STATUS"),
        save_figure=settings.get("MAP_SAVE_FIGURE", True),
        map_save_name=settings.get("MAP_SAVE_NAME", "PLOT_MAP.html"),
        dict_icons=None,
        validator_marker_cluster=settings.get("VALIDATOR_MARKER_CLUSTER", True),
        column_marker_cluster=settings.get("COLUMN_MARKER_CLUSTER", "state"),
        column_latitude=settings.get("COLUMN_LATITUDE", "lat"),
        column_longitude=settings.get("COLUMN_LONGITUDE", "long"),
        name_column_tooltip=settings.get("MAP_COLUMN_TOOLTIP", "name"),
        name_column_header=settings.get("MAP_COLUMN_HEADER", "name"),
    )
