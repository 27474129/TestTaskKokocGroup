ЗАПУСК: docker-compose up --build

.env файл не заигнорен осознанно для упрощения проверки

Слои абстракций отсутствуют т.к. это тестовое задание и сам проект маленький

Я имею ввиду что вся логика, в том числе ORM запросы, находятся в классах представлений, это сделано осознанно

При перезапуске контейнеров или ребилде нужно удалять тома
