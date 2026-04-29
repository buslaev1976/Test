#!/bin/bash
set -e

echo "========================================="
echo "MySQL Entrypoint Script"
echo "========================================="

# Запускаем MySQL
mysqld --user=mysql --datadir=/var/lib/mysql --skip-networking &
MYSQL_PID=$!

# Ждём готовности
echo "Waiting for MySQL..."
sleep 10

# Выполняем init.sql (всегда, безопасно)
if [ -f "/docker-entrypoint-initdb.d/init.sql" ]; then
    echo "Executing init.sql..."
    mysql -u root < /docker-entrypoint-initdb.d/init.sql
    echo "✅ init.sql executed"
fi

# Останавливаем временный MySQL
kill $MYSQL_PID
wait $MYSQL_PID 2>/dev/null

# Запускаем основной MySQL
exec mysqld --user=mysql --datadir=/var/lib/mysql --bind-address=0.0.0.0
