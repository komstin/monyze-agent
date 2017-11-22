# monyze-agent
MONYZE monitoring agent

================== Russian ===================

## Агент для сервиса Monyze - приложение на Питоне, собирающее системные метрики для сервиса https://monyze.ru/. 

Версия 0.0.6 (22.11.2017)

Обмен с сервером по заданному (нестандартному) протоколу в формате json. Не RESTful.

Работа на заказ. Не закончена, в процессе.

Для запуска демона предназначен модуль monyze-agent, расположенный в фолдере dist/. Модуль скомпилирован с помощью PyInstaller с параметром -F (упаковка одним файлом) и key=... Последнее - для пользователей, которые не ищут источники на Гитхабе.

`chmod +x monyze-agent`

`./monyze-agent --help`

```
usage: monyze [-h] [-c {show,delete}] [-a {start,stop,restart,status}]
              [-t TIMEOUT] [-u USERID] [-v]
```
Мониторинг Monyze

#### Параметры командной строки:

```
Без параметров (sudo) - запуск сервиса

-h, --help
      Показать подсказку
-c {show, delete}, --config {show, delete}
      Конфигурация: показать, удалить
-t TIMEOUT, --timeout TIMEOUT
      Задать временной интервал мониторинга в секундах
-u USERID, --userid USERID
      Задать userId
-v, --version
      Показать версию и выйти
```

Подробнее - на сайте https://monyze.ru

#### TODO List for Monyze Project

- [x] Setup request in preassigned format
- [x] Collect & update system data
- [x] Compile in one file
- [x] Daemonize
- [x] Setup as a service
- [x] Logging
- [ ] Extend for misc Linux'es

#### Extra TODO
- [ ] Расширить на Windows-платформу.
- [ ] Желательно: переделать Backend, сменить протокол на REST.
- [ ] Лучше всего радикально реконструировать архитектуру.
