# TUI_Dadata_API

## О проекте
Программа для поиска координат по адресу с функцией подсказок через сервис [dadata.ru](https://dadata.ru/profile/#info).  
Интерфейс терминала реализован с помощью библиотеки [npyscreen 4.10.5](https://pypi.org/project/npyscreen/4.10.5/).  
В данном репозитории находится доработанная версия npyscreen, с возможностью ввода кириллицы в терминал.

## Инструкция
### 1. Регистрация в сервисе Dadata
Для получения API-ключа Вам необходимо зарегистрироваться в сервисе, после чего необходимые данные будут доступны в Вашем личном кабинете по ссылке: [dadata.ru](https://dadata.ru/profile/#info).  
### 2. Скачать и запустить программу
Необходимо скачать и запустить скомпилированный файл из репозитория - [DadataAPI.exe](https://github.com/AlexMal923/TUI_Dadata_API/raw/master/DadataAPI.exe)
### 3. Настройка и навигация
При первом запуске необходимо ввести полученный на первом этапе API-ключ.  
Также можно настроить язык поиска и количество похожих адресов по Вашему запросу, которое будет показано в терминале.  
В папке с программой **DadataAPI.exe** будет создан файл `config.db` для сохранения настроек языка и API-ключа.

Чтобы вставить текст в поле терминала, используйте комбинацию клавиш <kbd>**Ctrl**</kbd> + <kbd>**Shift**</kbd> + <kbd>**V**</kbd>.  
Навигация в программе осуществляется с помощью стрелок <kbd>🠈</kbd><kbd>🠊</kbd><kbd>🠉</kbd><kbd>🠋</kbd> и клавиши <kbd>**Enter**</kbd>.  


![2022-07-27 (10)](https://user-images.githubusercontent.com/84757904/181282692-66630de4-1240-4d4c-8a52-36d8e147fe13.png)

### 4. Функционал
Введите адрес в указанное на картинке поле и нажмите <kbd>**Enter**</kbd>.  

![2022-07-27 (7)](https://user-images.githubusercontent.com/84757904/181279083-7b4fae5b-7d95-4d45-8f38-5e312a3b3d9b.png)

Выберите интересующий Вас адрес среди предложенных рекомендаций и нажмите <kbd>**Enter**</kbd> для получения координат.

![2022-07-27 (8)](https://user-images.githubusercontent.com/84757904/181279107-4b38c702-8181-43da-ad87-a8af88c7e127.png)

После повторного нажатия <kbd>**Enter**</kbd> программа вернется к поиску по адресу.

### 5. Завершение работы
Для выхода из программы нажмите клавишу <kbd>**Esc**</kbd> или кнопку **`Выход`** в терминале.  
Действующий API-ключ сохранится и будет загружен при повторном запуске программы.
