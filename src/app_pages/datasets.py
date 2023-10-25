import os
from pathlib import Path
from inspect import stack

import pandas as pd
import streamlit as st
from loguru import logger
from config_app.config_app import settings
from utils.dataframe_explorer import dataframe_explorer

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

	if "dataset" not in st.session_state.keys():

		# OBTENDO OS DADOS DE ESTAÇÕES METEOROLÓGICAS
		dir_measurements = settings.get("DATA_DIR_STATIONS")
		data = pd.read_excel(str(Path(dir_root, dir_measurements)))

		logger.info("DADOS OBTIDOS COM SUCESSO")

		st.session_state["dataset"] = data

	else:
		logger.info(
			"df_planejamento - DADOS RECUPERADOS DO SESSION STATE COM SUCESSO - {} AGÊNCIAS".format(
				len(st.session_state["dataset"])
			)
		)

		data = st.session_state["dataset"]

	if "selected_df" not in st.session_state.keys():

		# CARREGANDO DATAFRAME
		st.session_state["selected_df"] = st.session_state["dataset"]

	else:
		logger.info(
			"selected_df - DADOS RECUPERADOS DO SESSION STATE COM SUCESSO - {} ESTAÇÕES".format(
				len(st.session_state["selected_df"])
			)
		)

	# CRIANDO O SELECT BOX DE DATASETS
	st.session_state["list_datasets"] = settings.get("LIST_DATASETS")

	st.session_state["filtro_dataset"] = st.selectbox(
		label="Datasets",
		options=st.session_state["list_datasets"],
	)

	# OBTENDO O DATAFRAME
	dataframe_explorer_type, dataframe_return = convert_dataframe_explorer(
		data=st.session_state["selected_df"],
		style=settings.get("OPTION_DATAFRAME_EXPLORER",
						   "dataframe_explorer"),
	)

	# INCLUINDO O DATAFRAME
	selected_df = st.dataframe(dataframe_return, use_container_width=True)
	# OBTENDO O DATAFRAME DAS LINHAS SELECIONADAS
	st.session_state["selected_df"] = dataframe_return