import npyscreen
from dadata_api import DadataClient, request_errors
from curses import ascii
from database import DatabaseClient


class ButtonSearch(npyscreen.ButtonPress):
    """Кнопка для авторизации и перехода к форме поиска"""
    def whenPressed(self):
        self.parent.parentApp.getForm('MAIN').start_search()


class ButtonConfig(npyscreen.ButtonPress):
    """Кнопка возврата к настройкам"""
    def whenPressed(self):
        self.parent.parentApp.switchForm('MAIN')


class ButtonExit(npyscreen.ButtonPress):
    """Кнопка выхода"""
    def whenPressed(self):
        self.parent.parentApp.exit()


class ButtonAddress(npyscreen.ButtonPress):
    """Кнопка со строкой адреса для получения координат"""
    def whenPressed(self):
        index = int(self.name[:2]) - 1
        address = self.parent.parentApp.my_client.suggestions[index]
        latitude = address.get('data', {}).get('geo_lat', 'error')
        longitude = address.get('data', {}).get('geo_lon', 'error')
        if not any([geo is None for geo in [latitude, longitude]]):
            npyscreen.notify_confirm(f'{self.name}\n{latitude, longitude}', title='Координаты (широта, долгота)')
        else:
            npyscreen.notify_confirm(f'{self.name}\nНе удалось получить координаты :(', title='Координаты (ошибка)')
        self.parent.parentApp.getForm('Search').clear_form()


class SetConfig(npyscreen.FormBaseNew):
    """Форма для получение/добавление/обновление конфигураций с последующей авторизацией в сервисе dadata"""
    def create(self):
        self.user_token = ''
        self.user_language = 'ru'
        self.user_config = self.parentApp.my_database.get()
        if self.user_config:
            self.user_token = self.user_config[0][1]
            self.user_language = self.user_config[0][2]

        self.token = self.add(npyscreen.TitleText, name='API-ключ:', value=self.user_token, use_two_lines=False)
        self.sug_size = self.add(npyscreen.TitleSlider, name='Кол-во адресов в подсказке:', value=10, rely=5,
                                 lowest=2, out_of=20, use_two_lines=True)
        self.language = self.add(npyscreen.TitleSelectOne, name='Язык поиска адреса:',
                                 value='en' == self.user_language, values=['ru', 'en'], scroll_exit=True, rely=8)
        self.search_button = self.add(ButtonSearch, name='Перейти к поиску', rely=12, relx=40)
        self.exit_button = self.add(ButtonExit, name='Выход', rely=13, relx=40)
        # exit handlers
        exit_handler = self.parentApp.exit_handler
        self.add_handlers(exit_handler)
        self.token.add_handlers(exit_handler)
        self.token.add_handlers({ascii.CR: self.start_search})
        self.sug_size.add_handlers(exit_handler)
        self.language.add_handlers(exit_handler)
        self.search_button.add_handlers(exit_handler)
        self.exit_button.add_handlers(exit_handler)

    def start_search(self, _input=None):
        self.parentApp.my_client.token = self.token.value
        self.parentApp.my_client.sug_size = int(self.sug_size.value)
        self.parentApp.my_client.language = ['ru', 'en'][self.language.value[0]]
        if any([ord('А') <= ord(i) <= ord('я') for i in self.parentApp.my_client.token]):
            npyscreen.notify_confirm(f"Произошла ошибка:\nAPI-ключ содержит недопустимые символы", title="Упс!", wrap=True, editw=1)
            return
        auth_passed, err = self.parentApp.my_client.log_in()
        if auth_passed:
            if not self.user_config:
                self.parentApp.my_database.add(token=self.parentApp.my_client.token,
                                               language=self.parentApp.my_client.language)
            elif self.token.value != self.user_token or self.parentApp.my_client.language != self.user_language:
                self.parentApp.my_database.update(token=self.parentApp.my_client.token,
                                                  language=self.parentApp.my_client.language)
            self.parentApp.switchForm('Search')
        else:
            error = request_errors.get(err.response.status_code, 'Произошла внутренняя ошибка сервиса')
            npyscreen.notify_confirm(f"Произошла ошибка:\n{error}", title="Упс!", wrap=True, editw=1)


class SearchAddress(npyscreen.FormBaseNew):
    """Форма поиска адреса"""
    def search(self, _input):
        search_address = self.address.value
        self.address.value = ''
        result, err = self.parentApp.my_client.get_suggestions(search_address)
        if result:
            self.parentApp.addForm('Suggestions', Suggestions, name=search_address, columns=250)
            self.parentApp.getForm('Suggestions').set_buttons()

            self.parentApp.switchForm('Suggestions')
        else:
            npyscreen.notify_confirm(f'Не получилось найти адрес:\n{err or "Такого адреса нет"}', title="Упс!",
                                     wrap=True)

    def clear_form(self):
        self.parentApp.switchForm('Search')
        self.parentApp.removeForm('Suggestions')

    def create(self):
        self.address = self.add(npyscreen.TitleText, name='Введите адрес:', value='', use_two_lines=False)
        self.to_config_button = self.add(ButtonConfig, name='Настройки', relx=40, rely=4)
        self.exit_button = self.add(ButtonExit, name='Выход', relx=40, rely=5)

        # exit handlers
        exit_handler = self.parentApp.exit_handler
        self.add_handlers(exit_handler)
        self.to_config_button.add_handlers(exit_handler)
        self.exit_button.add_handlers(exit_handler)
        self.address.add_handlers(exit_handler)
        self.address.add_handlers({ascii.CR: self.search})  # enter key action


class Suggestions(npyscreen.FormBaseNew):
    """Форма для получения координат по выбранному адресу из списка подсказок"""
    def set_buttons(self):
        exit_handler = self.parentApp.exit_handler
        result = self.parentApp.my_client.suggestions
        for i in range(len(result)):
            self.add(ButtonAddress,
                         name=f"{str(i + 1).rjust(2)}. {result[i].get('value', '')}").add_handlers(exit_handler)
        self.search_button = self.add(ButtonSearch, name='Назад к поиску', relx=40)
        self.exit_button = self.add(ButtonExit, name='Выход', relx=40)
        self.exit_button.add_handlers(exit_handler)
        self.search_button.add_handlers(exit_handler)


class MyApplication(npyscreen.NPSAppManaged):
    """Менеджер приложений"""
    def exit(self):
        exit(0)

    def onStart(self):
        self.exit_handler = {ascii.ESC: self.exit}
        self.my_database = DatabaseClient()
        self.my_client = DadataClient()
        self.addForm('MAIN', SetConfig, name='Настройка конфигурации')
        self.addForm('Search', SearchAddress, name='Поиск по адресу')
