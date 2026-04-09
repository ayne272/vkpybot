#!/bin/bash
# Скрипт для скачивания бэкапов PostgreSQL из Kubernetes

set -e

NAMESPACE="vkbot"
BACKUP_DIR="./backups"

echo "=== Скачивание бэкапа PostgreSQL ==="
echo

# Создать локальную директорию для бэкапов
mkdir -p "$BACKUP_DIR"

# Получить имя пода postgres
POD=$(kubectl get pod -n $NAMESPACE -l app=postgres -o jsonpath='{.items[0].metadata.name}')

if [ -z "$POD" ]; then
    echo "Ошибка: Под postgres не найден в namespace $NAMESPACE"
    exit 1
fi

echo "Найден под: $POD"
echo

# Показать список доступных бэкапов
echo "Доступные бэкапы:"
kubectl exec -n $NAMESPACE $POD -- ls -lh /backups/ 2>/dev/null | grep vkbot_ || {
    echo "Бэкапы не найдены. Возможно CronJob еще не выполнялся."
    echo "Запустите вручную: kubectl create job --from=cronjob/postgres-backup manual-backup -n vkbot"
    exit 1
}

echo
read -p "Введите имя файла для скачивания: " BACKUP_FILE

if [ -z "$BACKUP_FILE" ]; then
    echo "Имя файла не указано"
    exit 1
fi

# Скачать бэкап
echo "Скачивание $BACKUP_FILE..."
kubectl cp $NAMESPACE/$POD:/backups/$BACKUP_FILE $BACKUP_DIR/$BACKUP_FILE

if [ $? -eq 0 ]; then
    echo
    echo "✓ Бэкап успешно скачан: $BACKUP_DIR/$BACKUP_FILE"
    ls -lh $BACKUP_DIR/$BACKUP_FILE
else
    echo "✗ Ошибка при скачивании бэкапа"
    exit 1
fi
