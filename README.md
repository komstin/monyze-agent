# monyze-agent
MONYZE monitoring agent

================== Russian ===================

Агент для сервиса Monyze - https://monyze.ru/ Версия 0.0.3

Обмен с сервером по заданному (нестандартному) протоколу. Не RESTful.

Работа на заказ. Не закончена, в процессе.

Запуск:

Модуль monyze-agent в /dist

chmod +x monyze-agent

./monyze-agent --help

TODO:
1. Сделать запуск сервисом.
2. Пока сделано для Debian/Ubuntu, расширить на другие Linux-платформы.
3. Расширить на Windows-платформу.
4. Желательно: переделать Backend, сменить протокол на REST.
5. Лучше всего радикально реконструировать архитектуру.
