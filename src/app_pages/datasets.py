import os
from pathlib import Path
from inspect import stack

import pandas as pd
import streamlit as st
from loguru import logger
from config_app.config_app import settings
from utils.pandas_functions import load_data
from utils.dataframe_explorer import dataframe_explorer
from utils.config_dataframe_explorer import COLUMN_CONFIG_DATASET_GHCN, COLUMN_CONFIG_DATASET_INMET

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

	# CRIANDO O MARKDOWN DE TÍTULO
	st.markdown("# {}".format(settings.get("APPNAME_TITLE",
										   "TG UFABC - ENERGIA - PREVISORES")))
	st.markdown(
		"Conjuntos de dados - Dados climáticos")

	# CRIANDO O SELECT BOX DE DATASETS
	st.session_state["list_datasets"] = settings.get("LIST_DATASETS")

	st.session_state["filtro_dataset"] = st.selectbox(
		label="Conjunto de dados",
		options=st.session_state["list_datasets"],
	)

	if st.session_state["filtro_dataset"] == "GHCN":
		dir_measurements = settings.get("DATA_DIR_STATIONS_GHCN")
	elif st.session_state["filtro_dataset"] == "INMET":
		dir_measurements = settings.get("DATA_DIR_STATIONS_INMET")

	if dir_measurements:

		# OBTENDO OS DADOS DE ESTAÇÕES METEOROLÓGICAS
		dir_measurements = settings.get("DATA_DIR_STATIONS_GHCN")
		data = load_data(str(Path(dir_root, dir_measurements)))

		logger.info("DADOS OBTIDOS COM SUCESSO")

		# SALVANDO EM DATASET
		st.session_state["dataset"] = data.get("DATAFRAME_RESULT")

		# OBTENDO O DATAFRAME
		dataframe_explorer_type, dataframe_return = convert_dataframe_explorer(
			data=st.session_state["dataset"],
			style=settings.get("OPTION_DATAFRAME_EXPLORER",
							   "dataframe_explorer"),
		)

		if st.session_state["filtro_dataset"] == "GHCN":

			# OBTENDO A CONFIG DAS COLUNAS
			COLUMN_CONFIG = COLUMN_CONFIG_DATASET_GHCN

			# OBTENDO SE HÁ ORDEM DAS COLUNAS
			list_columns_order = settings.get("LIST_COLUMNS_ORDER_GHCN",
											  dataframe_return.columns)

			dataframe_return = dataframe_return[list(list_columns_order)]

		elif st.session_state["filtro_dataset"] == "INMET":

			# OBTENDO A CONFIG DAS COLUNAS
			COLUMN_CONFIG = COLUMN_CONFIG_DATASET_INMET

			# OBTENDO SE HÁ ORDEM DAS COLUNAS
			list_columns_order = settings.get("LIST_COLUMNS_ORDER_INMET",
											  dataframe_return.columns)

			dataframe_return = dataframe_return[list(list_columns_order)]

		# INCLUINDO O DATAFRAME
		selected_df = st.dataframe(dataframe_return,
								   use_container_width=True,
								   column_config=COLUMN_CONFIG,
								   hide_index=True)

		# OBTENDO O DATAFRAME DAS LINHAS SELECIONADAS
		st.session_state["selected_df"] = dataframe_return

		# QUANTIDADE DE DADOS SELECIONADOS
		st.text("Quantidade de medições: {}".format(len(st.session_state["selected_df"])))

	else:
		logger.error("OPÇÃO NÃO VÁLIDA")