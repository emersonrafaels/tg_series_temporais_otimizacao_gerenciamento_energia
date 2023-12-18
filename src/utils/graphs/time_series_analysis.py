import numpy as np
import pandas as pd
import sidetable
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

from statsmodels.graphics.tsaplots import plot_acf

def plot_mean_variance_over_time(dataset, analysis_variable, n_chunks=20, name_analysis_variable=""):

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

      # OBTENDO A MÉDIA GLOBAL
      mean_global = dataset[analysis_variable].mean()

      # OBTENDO A VARIÂNCIA GLOBAL
      variance_global = (dataset[analysis_variable].var())

      # DIVINDO OS DADOS EM UM ARBITRÁRIO NÚMERO DE PARTES (CHUNKS)
      df_unique_station_chunks = np.array_split(dataset[analysis_variable], n_chunks)

      # INICIANDO AS VARIÁVEIS AUXILIARES
      means, variances = [], []

      # OBTENDO A MÉDIA E A VARIÂNCIA DE CADA PARTE (CHUNK)
      for chunk in df_unique_station_chunks:
          means.append(np.mean(chunk))
          variances.append((np.var(chunk)))

      # Plot
      plt.title('Comparando média e variância ao longo do tempo \nEstação Metereológica: {} - \nVariável {}'.format(dataset["name"].unique()[0],
                                                                                                                    name_analysis_variable),
                size=15)
      plt.plot(np.arange(len(means)), [mean_global] * len(means), label='Média global', lw=1.5)
      plt.scatter(x=np.arange(len(means)), y=means, label='Média', s=100)
      plt.plot(np.arange(len(variances)), [variance_global] * len(variances), label='Variância global', lw=1.5, color='orange')
      plt.scatter(x=np.arange(len(variances)), y=variances, label='Variância', color='orange', s=100)


      # DEFININDO O YAXIS E XAXIS RANGE
      plt.ylim(-1, max(variances + means)*1.2)
      plt.xlim(-1, len(means)*1.1)

      plt.legend()

      return plt, mean_global, variance_global, means, variances