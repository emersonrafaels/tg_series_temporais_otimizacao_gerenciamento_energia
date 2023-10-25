import os

import streamlit as st

from config_app.config_app import settings
from utils.streamlit_functions import add_logo
from app_pages.forecasts import load_forecast
from app_pages.datasets import load_datasets

# CONFIGURANDO O APP
st.set_page_config(
    page_title=settings.get("APPNAME_TITLE",
                            "TG UFABC - ENERGIA - PREVISOR DE GERAÇÃO DE ENERGIA"),
    page_icon=settings.get("APPNAME_TITLE_ICON",
                           ":factory:"),
    layout="wide",
)

def load_app():

	with st.sidebar:

		# OBTENDO O DIRETÓRIO DO LOGO
		dir_logo = settings.get("LOGO_APP")

		# ADICIONANDO LOGO
		add_logo(dir_logo, width=210, location="sidebar", position_image="left")

		st.markdown("Bem vindo(a): {}".format(os.environ.get("username")))

		# CRIANDO UMA LINHA EM BRANCO
		st.divider()

		# ESTUDO DESEJADO
		st.title("Escolha a página desejada")

		# COMBOBOX PARA O ESTUDO DESEJADO
		options_estudos = [
			"Modelos de previsão",
			"Datasets",
		]

		selected_estudo_desejado = st.radio(
			label="Estudo desejado",
			options=options_estudos,
			index=0,
			key=None,
			help="Escolha o estudo desejado e na página central aparecerão novas informações",
			on_change=None,
			disabled=False,
			horizontal=False,
			label_visibility="visible",
		)

		# DEFININDO A PÁGINA DESEJADA
		if selected_estudo_desejado == "Modelos de previsão":
			# CARREGANDO A PÁGINA DE AUTOSSERVIÇO
			load_forecast()

		elif selected_estudo_desejado == "Datasets":
			# CARREGANDO A PÁGINA DE AGÊNCIAS
			load_datasets()

		else:
			st.empty()

	st.markdown("# {}".format(settings.get("APPNAME_TITLE",
										   "TG UFABC - ENERGIA - PREVISORES")))
	st.markdown("Prevendo geração e carga no Sistema Interligado Nacional (SIN)")