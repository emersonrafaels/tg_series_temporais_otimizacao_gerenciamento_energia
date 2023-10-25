from inspect import stack

import pandas as pd
import plotly.express as px
from loguru import logger


def create_graph_timeseries_datasets(
    data, groupby_column, column_x_axis, column_y_axis, fig_title=""
):
    """

    REALIZA O PLOT DE UMA SÉRIE TEMPORAL
    PARA O DATASET DE MEDIÇÕES
    CLIMÁTICAS

    # Arguments
            data               - Required: Dados para plotar (Dataframe)
            groupby_column     - Required: Coluna para agrupar os dados (String | List)
            column_x_axis      - Required: Nome da variável que estará na coluna x (String)
            column_y_axis      - Required: Nome da variável que estará na coluna y (String)
            fig_title          - Optional: Nome do título para a figura (String)

    # Returns
            fig                - Required: Figura para plotar (Fig Plotly)

    """

    try:
        # VERIFICANDO SE DATA É UM DATAFRAME
        if isinstance(data, pd.DataFrame):
            # VERIFICANDO SE O VALOR DA COLUNA É UMA STRING
            if isinstance(groupby_column, str):
                if groupby_column in data.columns:
                    data_group = data.groupby(by=[groupby_column]).mean().reset_index()
                    name_column_group = groupby_column
            else:
                data_group = data.groupby(by=groupby_column).mean().reset_index()
                name_column_group = groupby_column[0]

            # OBTENDO A SÉRIE TEMPORAL
            fig = px.line(
                data_group,
                x=column_x_axis,
                y=column_y_axis,
                color=name_column_group,
                title=fig_title,
            )

            fig.update_xaxes(rangeslider_visible=True)

            return fig

    except Exception as ex:
        logger.warning("ERRO NA FUNÇÃO {} - {}".format(stack()[0][3], ex))
