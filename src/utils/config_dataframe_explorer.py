import streamlit as st

COLUMN_CONFIG_DATASET_GHCN = {
    "measurement date": st.column_config.DatetimeColumn(
        "measurement date",
        help="Data de medição",
        format="DD/MM/YYYY",
    ),
    "name": st.column_config.TextColumn(
        "name",
        help="Nome da estação metereológica",
    ),
    "state": st.column_config.TextColumn(
        "state",
        help="Estado brasileira onde está localizada a estação metereológica",
    ),
    "station": st.column_config.NumberColumn(
        "station",
        help="ID da estação metereológica",
        format="%d",
    ),
    "year": st.column_config.NumberColumn(
        "year",
        help="Ano de medição",
        format="%d",
        step=1,
    ),
    "month": st.column_config.NumberColumn(
        "month",
        help="Mês de medição",
        format="%d",
        step=1,
    ),
    "avg_temp": st.column_config.NumberColumn(
        "avg_temp",
        help="Temperatura média",
        format="%d",
    ),
    "avg_awnd": st.column_config.NumberColumn(
        "avg_awnd",
        help="Velocidade do vento média",
        format="%d",
    ),
    "avg_prcp": st.column_config.NumberColumn(
        "avg_prcp",
        help="Precipitação média",
        format="%d",
    ),
    "lat": st.column_config.NumberColumn(
        "lat",
        help="Latitude",
        format="%f",
    ),
    "long": st.column_config.NumberColumn(
        "long",
        help="Longitude",
        format="%f",
    ),
    "elev": st.column_config.NumberColumn(
        "elev",
        help="Elevação da estação metereológica",
        format="%f",
    ),
    "city": st.column_config.TextColumn(
        "city",
        help="Cidade brasileira onde está localizada a estação metereológica",
    ),
}

COLUMN_CONFIG_DATASET_INMET = {}
