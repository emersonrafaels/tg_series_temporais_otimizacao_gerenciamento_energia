import numpy as np


def remove_outliers(data, threshold=3):

	"""

	REMOVE OUTLIERS DE UM CONJUNTO DE DADOS, BASEADO NO DESVIO PADRÃO

	Arguments:
		data:                       - Required: Uma lista ou array contendo os dados de pressão.
												(List | Array)
		threshold:                  - Optional: Limiar para identificar outliers
												(padrão é 3 desvios padrão)
												(Integer)

	Returns:
		filtered_data               - Required: Lista ou array com outliers removidos
											    (List | Array)

	"""

	mean = np.mean(data)
	std_dev = np.std(data)
	filtered_data = [x for x in data if (
				mean - threshold * std_dev < x < mean + threshold * std_dev)]
	return filtered_data


def get_difference_list_values_versus_global_value(list_values,
												   global_value):

	"""

	CALCULA A DIFERENÇA DE UMA CADA VALOR, DE UMA LISTA DE VALORES,
	EM RELAÇÃO A UM ÚNICO VALOR.

	PODE SER USADA PARA CALCULAR A VARIAÇÃO DE UMA LISTA, EM RELAÇÃO
	A UMA MÉDIA GLOBAL OU VARIÂNCIA GLOBAL.

	Arguments:
		list_values:             - Required: Lista de valores numéricos para comparar
											 (List | Array)
		global_value:            - Optional: Valor numérico a ser comparado (Integer | Float)

	Returns:
		list_difference          - Required: Lista ou array com diferenças calculadas
											 (List | Array)

	"""

	list_difference = [abs((1 - (x / global_value))) for x in list_values]

	return list_difference