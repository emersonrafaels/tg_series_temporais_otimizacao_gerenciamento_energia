import os
from pathlib import Path

import pandas as pd

from src.config_app.config_app import settings

from src.utils.map.map_functions import load_map

# DEFININDO O DIRETÓRIO ROOT
dir_root = Path(__file__).absolute().parent.parent.parent

os.chdir(str(dir_root))

# OBTENDO OS DADOS DE ESTAÇÕES
dir_stations = 'data enrichment/data_station_with_result_api.xlsx'

data = pd.read_excel(str(Path(dir_root, dir_stations)))

# TORNANDO OS DADOS NULO EM "-", PARA MELHOR VISUALIZAÇÃO
data = data.fillna("-")

# ORDENANDO AS COLUNAS COMO DESEJADAS
data = data[settings.get("LIST_COLUMNS_ORDER")]

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
    column_latitude=settings.get("COLUMN_LATITUDE", "LATITUDE"),
    column_longitude=settings.get("COLUMN_LONGITUDE", "LONGITUDE"),
    name_column_tooltip=settings.get("MAP_COLUMN_TOOLTIP", "CÓDIGO AG"),
    name_column_header=settings.get("MAP_COLUMN_HEADER", "ENDEREÇO"),
)
