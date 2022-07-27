import sqlite3


class DatabaseClient(object):
    """Клиент для подключения к БД sqlite"""
    def __init__(self, db_filename="config.db", table_name='api_config'):
        """Создание БД и таблицы концигураций"""
        self.db_filename = db_filename
        self.table_name = table_name
        db = sqlite3.connect(self.db_filename)
        c = db.cursor()
        c.execute(
            f'''CREATE TABLE if NOT EXISTS {self.table_name} 
            (service_link Text DEFAULT 'https://dadata.ru/', 
            token text, 
            language text DEFAULT 'ru')'''
        )
        db.commit()
        c.close()

    def add(self, service_link='https://dadata.ru/', token='', language='ru'):
        """Добавление первой записи"""
        db = sqlite3.connect(self.db_filename)
        c = db.cursor()
        c.execute(f'INSERT INTO {self.table_name} VALUES (?, ?, ?)', (service_link, token, language))
        db.commit()
        c.close()

    def update(self, service_link='https://dadata.ru/', token='', language='ru'):
        """Обновление таблицы"""
        db = sqlite3.connect(self.db_filename)
        c = db.cursor()
        c.execute(f'UPDATE {self.table_name} SET service_link=?, token=?, language=?', (service_link, token, language))
        db.commit()
        c.close()

    def get(self):
        """Получение концигураций API"""
        db = sqlite3.connect(self.db_filename)
        c = db.cursor()
        c.execute(f'SELECT * FROM {self.table_name}')
        records = c.fetchall()
        c.close()
        return records
