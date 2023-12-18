import numpy as np


def remove_outliers(data, threshold=3):

	"""

	Remove outliers de um conjunto de dados baseado no desvio padrão.

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