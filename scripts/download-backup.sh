#!/bin/bash
# Скрипт для скачивания бэкапов PostgreSQL из Kubernetes

set -e

NAMESPACE="vkbot"
BACKUP_DIR="./backups"
REMOTE_SERVER="ayne@172.16.205.102"

echo "=== Скачивание бэкапа PostgreSQL ==="
echo

# Создать локальную директорию для бэкапов
mkdir -p "$BACKUP_DIR"

# Создать временный под для доступа к backup PVC
echo "Создание временного пода для доступа к бэкапам..."
ssh $REMOTE_SERVER "kubectl run backup-access --image=busybox --restart=Never -n $NAMESPACE --overrides='{
  \"spec\": {
    \"containers\": [{
      \"name\": \"backup-access\",
      \"image\": \"busybox\",
      \"command\": [\"sleep\", \"300\"],
      \"volumeMounts\": [{\"name\": \"backups\", \"mountPath\": \"/backups\"}]
    }],
    \"volumes\": [{\"name\": \"backups\", \"persistentVolumeClaim\": {\"claimName\": \"backup-pvc\"}}]
  }
}' 2>/dev/null || echo 'Pod already exists'"

# Дождаться запуска пода
echo "Ожидание запуска пода..."
ssh $REMOTE_SERVER "kubectl wait --for=condition=ready pod/backup-access -n $NAMESPACE --timeout=30s"

# Показать список доступных бэкапов
echo
echo "Доступные бэкапы:"
ssh $REMOTE_SERVER "kubectl exec -n $NAMESPACE backup-access -- ls -lh /backups/" | grep vkbot_ || {
    echo "Бэкапы не найдены."
    ssh $REMOTE_SERVER "kubectl delete pod backup-access -n $NAMESPACE"
    exit 1
}

echo
read -p "Введите имя файла для скачивания: " BACKUP_FILE

if [ -z "$BACKUP_FILE" ]; then
    echo "Имя файла не указано"
    ssh $REMOTE_SERVER "kubectl delete pod backup-access -n $NAMESPACE"
    exit 1
fi

# Скачать бэкап
echo "Скачивание $BACKUP_FILE..."
ssh $REMOTE_SERVER "kubectl cp $NAMESPACE/backup-access:/backups/$BACKUP_FILE /tmp/$BACKUP_FILE"
scp $REMOTE_SERVER:/tmp/$BACKUP_FILE $BACKUP_DIR/$BACKUP_FILE
ssh $REMOTE_SERVER "rm /tmp/$BACKUP_FILE"

# Удалить временный под
ssh $REMOTE_SERVER "kubectl delete pod backup-access -n $NAMESPACE"

echo
echo "✓ Бэкап успешно скачан: $BACKUP_DIR/$BACKUP_FILE"
ls -lh $BACKUP_DIR/$BACKUP_FILE
