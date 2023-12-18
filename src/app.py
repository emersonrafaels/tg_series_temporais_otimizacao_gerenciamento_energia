import os

import streamlit as st

from src.config_app.config_app import settings
from src.utils.streamlit_functions import add_logo
from src.app_pages.forecasts import load_forecast
from src.app_pages.datasets import load_datasets

# CONFIGURANDO O APP
st.set_page_config(
    page_title=settings.get(
        "APPNAME_TITLE", "TG UFABC - ENERGIA - PREVISOR DE GERAÇÃO DE ENERGIA"
    ),
    page_icon=settings.get("APPNAME_TITLE_ICON", ":factory:"),
    layout="wide",
)


def load_app():
    # APLICANDO O STYLE CSS
    st.markdown(
        """
		<style>
		#MainMenu {
			visibility:hidden;
		}
		footer{
			visibility:hidden;
		}
		footer:after{
			content: 'Feito por Emerson V. Rafael, com orientação da Prof. Dr(a). Patrícia Teixeira Leite Asano.';
			visibility:visible;
			display:block;
			position:relative;
			color:white;
			padding:5px;
			top:0px;
		}
		</style>
		""",
        unsafe_allow_html=True,
    )

    with st.sidebar:
        # OBTENDO O DIRETÓRIO DO LOGO
        dir_logo = settings.get("LOGO_APP")

        # ADICIONANDO LOGO
        add_logo(dir_logo, width=210, location="sidebar", position_image="left")

        st.markdown("Bem vindo(a): {}".format(os.environ.get("username",
                                                             "Visitante")))

        # CRIANDO UMA LINHA EM BRANCO
        st.divider()

        # ESTUDO DESEJADO
        st.title("Escolha a página desejada")

        # COMBOBOX PARA O ESTUDO DESEJADO
        options_estudos = [
            "Modelos de previsão",
            "Dados climáticos",
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

    elif selected_estudo_desejado == "Dados climáticos":
        # CARREGANDO A PÁGINA DE AGÊNCIAS
        load_datasets()

    else:
        st.empty()
