import numpy as np
import pandas as pd
import sidetable
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.stats.diagnostic import acorr_ljungbox


def get_mean_variance(dataset, analysis_variable, n_chunks=20):
    # OBTENDO A MÉDIA GLOBAL
    mean_global = dataset[analysis_variable].mean()

    # OBTENDO A VARIÂNCIA GLOBAL
    variance_global = dataset[analysis_variable].var()

    # DIVINDO OS DADOS EM UM ARBITRÁRIO NÚMERO DE PARTES (CHUNKS)
    df_unique_station_chunks = np.array_split(dataset[analysis_variable], n_chunks)

    # INICIANDO AS VARIÁVEIS AUXILIARES
    means, variances = [], []

    # OBTENDO A MÉDIA E A VARIÂNCIA DE CADA PARTE (CHUNK)
    for chunk in df_unique_station_chunks:
        means.append(np.mean(chunk))
        variances.append((np.var(chunk)))

    return mean_global, variance_global, means, variances


def plot_mean_variance_over_time(
    dataset,
    analysis_variable,
    n_chunks=20,
    name_analysis_variable="",
    width=10,
    height=3,
):
    """

    REALIZA O PLOT COMPARATIVO DA MÉDIA E VARIÂNCIA
    DE UM CONJUNTO DE DADOS AO
    LONGO DE UM PERÍODO DE TEMPO

    # Arguments
      dataset                 - Required: Conjunto de dados a ser analisado (DataFrame)
      analysis_variable       - Required: Variável de análise do dataframe, que será plotada
                                          A variável deve ser um valor numérico (String)
      n_chunks                - Optional: Quantidade de partes que os dados serão fragmentados.
                                          Cada parte representa um período de tempo
      name_analysis_variable  - Optional: Nome da variável de análise (String)

    # Returns
      means                   - Required: Lista com a média de cada parte (List)
      variances               - Required: Lista com a variância de cada parte (List)

    """

    # ANALISANDO SE O DATASET É UM DATAFRAME E SE A VARIÁVEL DE ANÁLISE CONSTA NESSE DATAFRAME
    if isinstance(dataset, pd.DataFrame):
        if analysis_variable in dataset.columns:
            # OBTENDO OS VALORES DE MÉDIA (GLOBAL E POR CHUNK) E VARIÂNCIA (GLOBAL E POR CHUNK)
            mean_global, variance_global, means, variances = get_mean_variance(
                dataset=dataset, analysis_variable=analysis_variable, n_chunks=n_chunks
            )

            # DEFININDO TAMANHO DA FIGURA
            plt.figure(figsize=(width, height))

            # Plot
            plt.title("Comparando média e variância ao longo do tempo", size=15)
            plt.plot(
                np.arange(len(means)),
                [mean_global] * len(means),
                label="Média global",
                lw=1.5,
            )
            plt.scatter(x=np.arange(len(means)), y=means, label="Média", s=100)
            plt.plot(
                np.arange(len(variances)),
                [variance_global] * len(variances),
                label="Variância global",
                lw=1.5,
                color="orange",
            )
            plt.scatter(
                x=np.arange(len(variances)),
                y=variances,
                label="Variância",
                color="orange",
                s=100,
            )

            # DEFININDO O YAXIS E XAXIS RANGE
            plt.ylim(-1, max(variances + means) * 1.2)
            plt.xlim(-1, len(means) * 1.1)

            # INCLUINDO LEGENDA
            plt.legend()

            return plt, mean_global, variance_global, means, variances


def test_ljung_box(data, n_lags=10):
    """

    VERIFICA SE UMA SÉRIE DE DADOS POSSUI AUTOCORRELAÇÃO

    SE O VALOR P (P-VALUE) FOR MAIOR QUE O NÍVEL DE SIGNIFICÂNCIA ESCOLHIDO
    (POR EXEMPLO, 0.05 OU 0.01), NÃO HÁ EVIDÊNCIA SUFICIENTE PARA REJEITAR A HIPÓTESE NULA.
    INTERPRETAÇÃO: NÃO HÁ AUTOCORRELAÇÃO SIGNIFICATIVA NOS DADOS ATÉ AS DEFASAGENS TESTADAS.

    SE O VALOR P FOR MENOR QUE O NÍVEL DE SIGNIFICÂNCIA ESCOLHIDO, A HIPÓTESE NULA É REJEITADA.
    INTERPRETAÇÃO: HÁ EVIDÊNCIAS DE AUTOCORRELAÇÃO NOS DADOS ATÉ AS DEFASAGENS TESTADAS.

    # Arguments
      data                           - Required: Dados a serem analisados (DataFrame)
      n_lags                         - Optional: Número de lags para analisar (Integer)

    # Returns
      result_test_ljung_box          - Required: Resultado do teste Ljung-Box (DataFrame)
      data_is_white_noise            - Required: Resultado da verificação se a curva é white noise (Boolean)

    """

    # Teste de Ljung-Box para verificar autocorrelação
    result_test_ljung_box = acorr_ljungbox(data, lags=n_lags)

    if not result_test_ljung_box[result_test_ljung_box["lb_pvalue"] > 0.05].empty:
        data_is_white_noise = True
    else:
        data_is_white_noise = False

    return result_test_ljung_box, data_is_white_noise


def validate_white_noise(dataset, analysis_variable, n_lags=10, n_chunks=20):
    """

    VALIDA SE UMA CURVA É WHITE NOISE

    # Arguments
      mean                  - Required:
      max_diff_mean         - Required:
      max_diff_var          - Required:

    # Returns

    """

    validator_white_noise = False

    # APLICANDO O TESTE DE LJUNG-BOX
    result_test_ljung_box, data_is_white_noise = test_ljung_box(
        data=dataset[analysis_variable], n_lags=n_lags
    )

    # OBTENDO OS VALORES ESTATÍSTICOS
    # OBTENDO OS VALORES DE MÉDIA (GLOBAL E POR CHUNK) E VARIÂNCIA (GLOBAL E POR CHUNK)
    mean_global, variance_global, means, variances = get_mean_variance(
        dataset=dataset, analysis_variable=analysis_variable, n_chunks=n_chunks
    )

    if data_is_white_noise == True:
        validator_white_noise = True

    return validator_white_noise
