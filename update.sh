#!/bin/bash

set -e

echo "🚀 Начинаем процесс обновления..."

# Проверка, что скрипт запущен в правильной папке
if [ ! -f "docker-compose.yml" ] &&[ ! -f "compose.yaml" ]; then
    echo "❌ Ошибка: Файл docker-compose.yml не найден. Запустите скрипт из папки проекта."
    exit 1
fi

echo "📦 1. Скачиваем свежий код из Git..."
git pull

echo "⬇️ 2. Скачиваем новые версии готовых образов..."
docker compose pull

echo "🔄 3. Пересобираем и перезапускаем контейнеры..."
docker compose up -d --build

echo "🧹 4. Удаляем старые (неиспользуемые) образы для экономии места..."
docker image prune -f

echo "✅ Проект успешно обновлен и работает!"