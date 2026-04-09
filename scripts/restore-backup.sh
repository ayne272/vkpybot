#!/bin/bash
# Скрипт для восстановления PostgreSQL из бэкапа

set -e

NAMESPACE="vkbot"
BACKUP_DIR="./backups"

echo "=== Восстановление PostgreSQL из бэкапа ==="
echo
echo "⚠️  ВНИМАНИЕ: Эта операция удалит все текущие данные в БД!"
echo

# Показать доступные локальные бэкапы
echo "Доступные локальные бэкапы:"
ls -lh $BACKUP_DIR/*.dump 2>/dev/null || {
    echo "Локальные бэкапы не найдены в $BACKUP_DIR"
    exit 1
}

echo
read -p "Введите имя файла для восстановления: " BACKUP_FILE

if [ -z "$BACKUP_FILE" ]; then
    echo "Имя файла не указано"
    exit 1
fi

# Проверить существование файла
if [ ! -f "$BACKUP_DIR/$BACKUP_FILE" ]; then
    echo "Ошибка: Файл $BACKUP_DIR/$BACKUP_FILE не найден"
    exit 1
fi

# Подтверждение
echo
read -p "Вы уверены что хотите восстановить БД из $BACKUP_FILE? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Отменено"
    exit 0
fi

# Получить имя пода postgres
POD=$(kubectl get pod -n $NAMESPACE -l app=postgres -o jsonpath='{.items[0].metadata.name}')

if [ -z "$POD" ]; then
    echo "Ошибка: Под postgres не найден в namespace $NAMESPACE"
    exit 1
fi

echo
echo "Найден под: $POD"
echo "Загрузка бэкапа в под..."

# Загрузить бэкап в под
kubectl cp $BACKUP_DIR/$BACKUP_FILE $NAMESPACE/$POD:/tmp/restore.dump

echo "Восстановление БД..."

# Восстановить БД
kubectl exec -n $NAMESPACE $POD -- sh -c '
    # Отключить активные соединения
    psql -U $POSTGRES_USER -d postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '\''$POSTGRES_DB'\'' AND pid <> pg_backend_pid();"

    # Удалить и пересоздать БД
    dropdb -U $POSTGRES_USER $POSTGRES_DB
    createdb -U $POSTGRES_USER $POSTGRES_DB

    # Восстановить из бэкапа
    pg_restore -U $POSTGRES_USER -d $POSTGRES_DB -v /tmp/restore.dump

    # Удалить временный файл
    rm /tmp/restore.dump
'

if [ $? -eq 0 ]; then
    echo
    echo "✓ БД успешно восстановлена из $BACKUP_FILE"
    echo
    echo "Перезапустите vkbot для применения изменений:"
    echo "kubectl rollout restart deployment vkbot -n $NAMESPACE"
else
    echo "✗ Ошибка при восстановлении БД"
    exit 1
fi
