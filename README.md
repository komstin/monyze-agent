# monyze-agent

MONYZE monitoring service agent

================== Russian ===================

### Агент для сервиса Monyze - приложение на Питоне, собирающее системные метрики для сервиса https://monyze.ru/. 

Версия 0.0.7 (26.11.2017)

Обмен с сервером по заданному (нестандартному) протоколу в формате json. Не RESTful.

Работа на заказ. Не закончена, в процессе.

Для запуска демона и контроля предназначен модуль monyze-agent, расположенный в фолдере dist/. Модуль скомпилирован с помощью PyInstaller с параметром -F (упаковка одним файлом) и key=... Последнее - для пользователей, которые не ищут источники на Гитхабе.

Для запуска:

`chmod +x monyze-agent`

Помощь:

`./monyze-agent --help`

```
usage: monyze [-h] [-c {show,delete}] [-v] [-t TIMEOUT] [-u USERID]
```

#### Параметры командной строки:

```
Без параметров - запуск сервиса (sudo)

-h, --help
      Показать подсказку
-c, --config
      Показать конфигурацию
-v, --version
      Показать версию
-t TIMEOUT, --timeout TIMEOUT
      Задать временной интервал
      мониторинга в секундах (sudo)
-u USERID, --userid USERID
      Задать userId (sudo)

Подробнее - на сайте https://monyze.ru
```

#### TODO List for Monyze Project

- [x] Setup request in preassigned format
- [x] Collect & update system data
- [x] Compile in one file
- [x] Daemonize
- [x] Setup as a service
- [x] Logging
- [ ] Extend for misc Linux'es

#### Extra TODO
- [ ] Expand for Windows
- [ ] Желательно: переделать Backend, сменить протокол на REST.
- [ ] Лучше всего радикально реконструировать архитектуру.
