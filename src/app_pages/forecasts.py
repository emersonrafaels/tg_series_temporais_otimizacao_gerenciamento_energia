import streamlit as st

from config_app.config_app import settings

def load_forecast():

	st.markdown("# {}".format(settings.get("APPNAME_TITLE",
										   "TG UFABC - ENERGIA - PREVISORES")))
	st.markdown(
		"Prevendo geração e carga no Sistema Interligado Nacional (SIN)")