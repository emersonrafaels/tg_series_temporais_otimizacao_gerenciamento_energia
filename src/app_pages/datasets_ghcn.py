import numpy as np
import pandas as pd
import streamlit as st
from loguru import logger

from src.utils.config_dataframe_explorer import (
    COLUMN_CONFIG_DATASET_GHCN,
)
from src.utils.map.map_functions import folium_static
from src.config_app.config_app import settings
from src.utils.graphs.graphs_datasets import create_graph_timeseries_datasets
from src.utils.graphs.time_series_analysis import plot_mean_variance_over_time, test_ljung_box, validate_white_noise
from src.utils.statistics_functions import (
    get_difference_list_values_versus_global_value,
)
from src.utils.map.map_app import plot_map_dataset_ghcn


def load_dataset_ghcn(dataframe_return):
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

    # TEMPERATURA
    column_timeseries_temp_axis = settings.get("COLUMN_TIMESERIES_TEMP_GHCN", "temp")

    # PRECIPITAÇÃO
    column_timeseries_prcp_axis = settings.get("COLUMN_TIMESERIES_PRCP_GHCN", "prcp")

    # VELOCIDADE DO VENTO
    column_timeseries_wdsp_axis = settings.get("COLUMN_TIMESERIES_WDSP_GHCN", "wdsp")

    # INCLUINDO O DATAFRAME
    selected_df = st.dataframe(
        dataframe_return,
        use_container_width=True,
        column_config=COLUMN_CONFIG,
        hide_index=True,
    )

    # OBTENDO O DATAFRAME DAS LINHAS SELECIONADAS
    st.session_state["selected_df"] = dataframe_return

    with st.expander(label="Metadados"):
        st.text("year - Representa o ano da medição")
        st.text(
            "month - Representa o mês da medição.\nDe 1 a 12, cada valor representa um dos meses do ano"
        )
        st.text(
            "day - Representa o dia da medição.\nDe 1 a 31, cada valor representa um dos dias do mês"
        )
        st.text("stn - Fornece o id da estação meteorológica")
        st.text("name - Fornece o nome da estação meteorológica")
        st.text(
            "country - Fornece o país da estação meteorológica\n(no caso, todos os dados referem-se ao Brasil)"
        )
        st.text("city - Fornece a cidade da estação meteorológica")
        st.text("state - Fornece o estado da estação meteorológica")
        st.text("lat - Latitude no qual a estação meteorológica está localizada")
        st.text("lon - Longitude no qual a estação meteorológica está localizada")
        st.text("begin - Data de início das medições na estação metereológica")
        st.text("end - Data de fim das medições na estação metereológica")
        st.text(
            "elev - Altura em média no qual a estação metereológica\nestá localizada, em relação ao nível do mar (m)"
        )
        st.text("temp - Temperatura média (C°)")
        st.text("prcp - Precipitação média (Pa)")
        st.text("wdsp - Velocidade média do vento (m/s)")
        st.text(
            "date_measurement - Valor em formato data que\nrepresenta o ano e mês dos dados medidos"
        )

    # QUANTIDADE DE DADOS SELECIONADOS
    st.text("Quantidade de medições: {}".format(len(st.session_state["selected_df"])))

    st.markdown("# 3. Distribuição das estações metereológicas")
    st.text(
        "- No mapa estão as estações metereológicas\napós os filtros aplicados no conjunto acima"
    )
    st.text(
        "- Utilize o zoom lateral, ou o zoom do mouse, para visualizar mais\n detalhes das estações metereológicas"
    )

    # PLOTANDO O MAPA DAS ESTAÇÕES METEREOLÓGICAS
    validator_map, st.session_state["mapobj"], _ = plot_map_dataset_ghcn(
        data=st.session_state["selected_df"]
    )

    st_data = folium_static(
        st.session_state["mapobj"],
        width=700,
        height=500,
        add_categorical_legend=False,
    )

    st.markdown("# 4. Séries temporais medidas no conjunto de dados")

    st.session_state["filter_dataset_group"] = st.selectbox(
        label="Selecione o modo de agrupamento",
        options=st.session_state["list_filter_dataset_group"],
    )

    # DEFININDO QUE O GROUPBY SERÁ PELA COLUNA ESCOLHA + A COLUNA PADRÃO
    filter_groupby = [st.session_state["filter_dataset_group"]] + [
        column_timeseries_x_axis
    ]

    # DEFININDO AS OPÇÕES PARA O FILTRO MULTISELECT DO GROUP
    options_group = (
        st.session_state["selected_df"][st.session_state["filter_dataset_group"]]
        .sort_values()
        .unique()
    )

    # CRIANDO MULTISELECT BASEADO NO FILTRO
    # SELECIONAR TIPO DE AGRUPAMENTO
    filter_groupby_value = st.multiselect(
        label="Selecione um ou mais valores para exibir",
        options=options_group,
        default=options_group[0],
        placeholder="Selecione um ou mais valores para exibir"
    )

    # FILTRANDO BASEADO NO MULTISELECT
    dataframe_plot = st.session_state["selected_df"][
        st.session_state["selected_df"][st.session_state["filter_dataset_group"]].isin(
            filter_groupby_value
        )
    ]

    st.markdown("## 4.1 Analisando as séries temporais")

    # REALIZANDO O PLOT DAS SÉRIES TEMPORAIS

    with st.expander("Temperatura"):
        # TEMPERATURA
        container_temp = st.container()

        container_temp.markdown("## 1. Curva ao longo do tempo")

        # OBTENDO A SÉRIE TEMPORAL
        fig = create_graph_timeseries_datasets(
            data=dataframe_plot,
            groupby_column=filter_groupby,
            column_x_axis=column_timeseries_x_axis,
            column_y_axis=column_timeseries_temp_axis,
            fig_title="Time Series - Temperatura (°C)",
        )

        # PLOTANDO A SÉRIE TEMPORAL
        container_temp.plotly_chart(figure_or_data=fig, use_container_width=True)

        container_temp.markdown("## 2. Analisando a curva - White Noise")

        # OBTENDO A ANÁLISE DE WHITE NOISE
        (
            plt,
            mean_global,
            variance_global,
            means,
            variances,
        ) = plot_mean_variance_over_time(
            dataset=dataframe_plot,
            analysis_variable=column_timeseries_temp_axis,
            n_chunks=20,
            name_analysis_variable="Temperatura",
        )

        # PLOTANDO A ANÁLISE DA MÉDIA E VARIÂNCIA AO LONGO DO TEMPO
        container_temp.pyplot(fig=plt, use_container_width=True)

        # OBTENDO A MÉDIA E A MÁXIMA DIFERENÇA
        list_difference = get_difference_list_values_versus_global_value(
            list_values=means, global_value=mean_global
        )

        container_temp.text(
            "Média: {} (C°)".format(
                round(np.mean(means), 2),
            )
        )

        container_temp.text(
            "Máxima variação de valor em relação à média: {}%".format(
                round(100 * np.max(list_difference), 2)
            )
        )

        # OBTENDO A MÁXIMA DIFERENÇA (VARIÂNCIA)
        list_difference = get_difference_list_values_versus_global_value(
            list_values=variances, global_value=variance_global
        )

        container_temp.text(
            "Máxima diferença em relação à variância: {}%".format(
                round(100 * np.max(list_difference)), 2
            )
        )

        # ANÁLISE DE AUTOCORRELAÇÃO - APLICANDO O TESTE DE LJUNG-BOX
        result_test_ljung_box, _ = test_ljung_box(data=dataframe_plot[column_timeseries_temp_axis],
                                                  n_lags=10)

        st.text("Teste de autocorrelação - Teste de Ljung-Box")
        st.dataframe(result_test_ljung_box, hide_index=True)

    with st.expander("Precipitação"):
        container_prcp = st.container()

        container_prcp.markdown("## 1. Curva ao longo do tempo")

        # PRECIPITAÇÃO
        fig = create_graph_timeseries_datasets(
            data=dataframe_plot,
            groupby_column=filter_groupby,
            column_x_axis=column_timeseries_x_axis,
            column_y_axis=column_timeseries_prcp_axis,
            fig_title="Time Series - Precipitação (Pa)",
        )

        container_prcp.plotly_chart(figure_or_data=fig, use_container_width=True)

        container_prcp.markdown("## 2. Analisando a curva - White Noise")

        # OBTENDO A ANÁLISE DE WHITE NOISE
        (
            plt,
            mean_global,
            variance_global,
            means,
            variances,
        ) = plot_mean_variance_over_time(
            dataset=dataframe_plot,
            analysis_variable=column_timeseries_prcp_axis,
            n_chunks=20,
            name_analysis_variable="Precipitação",
        )

        # PLOTANDO A ANÁLISE DA MÉDIA E VARIÂNCIA AO LONGO DO TEMPO
        container_prcp.pyplot(fig=plt, use_container_width=True)

        # OBTENDO A MÉDIA E A MÁXIMA DIFERENÇA
        list_difference = get_difference_list_values_versus_global_value(
            list_values=means, global_value=mean_global
        )

        container_prcp.text(
            "Média: {} Pa".format(
                round(np.mean(means), 2),
            )
        )

        container_prcp.text(
            "Máxima variação de valor em relação à média: {}%".format(
                round(100 * np.max(list_difference), 2)
            )
        )

        # OBTENDO A VARIÂNCIA E A MÁXIMA DIFERENÇA
        list_difference = get_difference_list_values_versus_global_value(
            list_values=variances, global_value=variance_global
        )

        container_prcp.text(
            "Máxima diferença em relação à variância: {}%".format(
                round(100 * np.max(list_difference)), 2
            )
        )

    with st.expander("Velocidade do vento"):
        container_wdsp = st.container()

        container_wdsp.markdown("## 1. Curva ao longo do tempo")

        # VELOCIDADE DO VENTO
        fig = create_graph_timeseries_datasets(
            data=dataframe_plot,
            groupby_column=filter_groupby,
            column_x_axis=column_timeseries_x_axis,
            column_y_axis=column_timeseries_wdsp_axis,
            fig_title="Time Series - Velocidade do vento (m/s)",
        )

        container_wdsp.plotly_chart(figure_or_data=fig, use_container_width=True)

        container_wdsp.markdown("## 2. Analisando a curva - White Noise")

        # OBTENDO A ANÁLISE DE WHITE NOISE
        (
            plt,
            mean_global,
            variance_global,
            means,
            variances,
        ) = plot_mean_variance_over_time(
            dataset=dataframe_plot,
            analysis_variable="wdsp",
            n_chunks=20,
            name_analysis_variable="Velocidade do vento",
        )

        # PLOTANDO A ANÁLISE DA MÉDIA E VARIÂNCIA AO LONGO DO TEMPO
        container_wdsp.pyplot(fig=plt, use_container_width=True)

        # OBTENDO A MÉDIA E A MÁXIMA DIFERENÇA
        list_difference = get_difference_list_values_versus_global_value(
            list_values=means, global_value=mean_global
        )

        container_wdsp.text(
            "Média: {} (m/s)".format(
                round(np.mean(means), 2),
            )
        )

        container_wdsp.text(
            "Máxima variação de valor em relação à média: {}%".format(
                round(100 * np.max(list_difference), 2)
            )
        )

        # OBTENDO A VARIÂNCIA E A MÁXIMA DIFERENÇA
        list_difference = get_difference_list_values_versus_global_value(
            list_values=variances, global_value=variance_global
        )

        container_wdsp.text(
            "Máxima diferença em relação à variância: {}%".format(
                round(100 * np.max(list_difference)), 2
            )
        )
