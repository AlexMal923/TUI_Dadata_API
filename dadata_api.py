from dadata import Dadata


class DadataClient:
	"""Клиент для подключения к Dadata и поиска адресов"""
	def __init__(self, token=''):
		self.token = token
		self.language = 'ru'
		self.sug_size = 10  # кол-во адресов в подсказке
		self.client = None
		self.suggestions = []

	def log_in(self):
		"""
		Авторизация по токену.
		:return: 	- Возвращает (True, None) при удачной авторизации, иначе (False, Exception)
		"""
		self.client = Dadata(self.token)
		try:
			self.client.get_versions()
		except Exception as e:
			return False, e
		else:
			return True, None

	def get_suggestions(self, address):
		"""
		Получение подсказок по введенному адресу
		:param address: str, адрес
		:return: 		Возвращает (List, None) при нахождении совпадений, иначе ([], Exception)
		"""
		try:
			self.suggestions = self.client.suggest("address", address, count=self.sug_size, language=self.language)
		except Exception as e:
			self.suggestions = []
			return self.suggestions, e
		else:
			return self.suggestions, None


request_errors = {
	400:	'Некорректный запрос (невалидный JSON или XML)',
	401:	'В запросе отсутствует API-ключ или в запросе указан несуществующий API-ключ',
	403:	'''В запросе указан несуществующий API-ключ
				Или не подтверждена почта
				Или исчерпан дневной лимит по количеству запросов''',
	405:	'Запрос сделан с методом, отличным от POST',
	413:	'Слишком большая длина запроса или слишком много условий',
	429:	'Слишком много запросов в секунду или новых соединений в минуту',
}

