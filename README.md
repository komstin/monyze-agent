# monyze-agent
MONYZE monitoring agent

================== Russian ===================

Агент для сервиса Monyze - приложение на Питоне, собирающее системные метрики для сервиса https://monyze.ru/. 

Версия 0.0.3

Обмен с сервером по заданному (нестандартному) протоколу в формате json. Не RESTful.

Работа на заказ. Не закончена, в процессе.

Для запуска демона предназначен модуль monyze-agent, расположенный в фолдере dist/

chmod +x monyze-agent

./monyze-agent --help

usage: monyze [-h] [-c {show,delete}] [-a {start,stop,restart,status}]
              [-t TIMEOUT] [-u USERID] [-v]

Мониторинг Monyze

optional arguments:

  -h, --help            Помощь
  
  -c {show,delete}, --config {show,delete}
                          Конфигурация: показать,
                          удалить
  -a {start,stop,restart,status}, --action {start,stop,restart,status}
                          Действие: запустить,
                          остановить, перезапустить,
                          статус
  -t TIMEOUT, --timeout TIMEOUT
                          Задать временной интервал
                          мониторинга в секундах
  -u USERID, --userid USERID
                          Задать userId
  -v, --version         Показать версию и выйти

Подробнее - на сайте https://monyze.ru

TODO:
1. Сделать запуск сервисом.
2. Пока сделано для Debian/Ubuntu, расширить на другие Linux-платформы.
3. Расширить на Windows-платформу.
4. Желательно: переделать Backend, сменить протокол на REST.
5. Лучше всего радикально реконструировать архитектуру.
