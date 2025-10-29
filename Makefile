.PHONY: help install run clean test lint format docker-build docker-run

# Цвета для вывода
BLUE := \033[0;34m
GREEN := \033[0;32m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Показать справку
	@echo "$(BLUE)Доступные команды:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'

install: ## Установить зависимости
	@echo "$(BLUE)Установка зависимостей...$(NC)"
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade pip
	. venv/bin/activate && pip install -r requirements.txt
	@echo "$(GREEN)✓ Зависимости установлены$(NC)"

install-dev: install ## Установить dev зависимости
	@echo "$(BLUE)Установка dev зависимостей...$(NC)"
	. venv/bin/activate && pip install black flake8 mypy pytest pytest-asyncio
	@echo "$(GREEN)✓ Dev зависимости установлены$(NC)"

run: ## Запустить бота
	@echo "$(BLUE)Запуск бота...$(NC)"
	. venv/bin/activate && python -m telegram_doc_bot.bot

clean: ## Очистить временные файлы
	@echo "$(BLUE)Очистка...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .pytest_cache/ .mypy_cache/
	rm -rf generated_docs/*.docx generated_docs/*.pdf
	@echo "$(GREEN)✓ Очистка завершена$(NC)"

format: ## Форматировать код с помощью black
	@echo "$(BLUE)Форматирование кода...$(NC)"
	. venv/bin/activate && black telegram_doc_bot/
	@echo "$(GREEN)✓ Код отформатирован$(NC)"

lint: ## Проверить код линтером
	@echo "$(BLUE)Проверка кода...$(NC)"
	. venv/bin/activate && flake8 telegram_doc_bot/ --max-line-length=100 --extend-ignore=E203,W503
	@echo "$(GREEN)✓ Проверка завершена$(NC)"

type-check: ## Проверить типы с помощью mypy
	@echo "$(BLUE)Проверка типов...$(NC)"
	. venv/bin/activate && mypy telegram_doc_bot/ --ignore-missing-imports
	@echo "$(GREEN)✓ Типы проверены$(NC)"

test: ## Запустить тесты
	@echo "$(BLUE)Запуск тестов...$(NC)"
	. venv/bin/activate && pytest tests/ -v
	@echo "$(GREEN)✓ Тесты пройдены$(NC)"

check: format lint type-check ## Выполнить все проверки

docker-build: ## Собрать Docker образ
	@echo "$(BLUE)Сборка Docker образа...$(NC)"
	docker build -t telegram-doc-bot .
	@echo "$(GREEN)✓ Образ собран$(NC)"

docker-run: ## Запустить в Docker
	@echo "$(BLUE)Запуск в Docker...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✓ Контейнер запущен$(NC)"

docker-stop: ## Остановить Docker контейнер
	@echo "$(BLUE)Остановка контейнера...$(NC)"
	docker-compose down
	@echo "$(GREEN)✓ Контейнер остановлен$(NC)"

docker-logs: ## Показать логи Docker контейнера
	docker-compose logs -f telegram-bot

setup: ## Первоначальная настройка проекта
	@echo "$(BLUE)Настройка проекта...$(NC)"
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "$(GREEN)✓ Создан файл .env$(NC)"; \
		echo "$(RED)⚠ Не забудьте добавить API ключи в .env!$(NC)"; \
	else \
		echo "$(GREEN)✓ Файл .env уже существует$(NC)"; \
	fi
	@mkdir -p generated_docs logs
	@echo "$(GREEN)✓ Директории созданы$(NC)"
	@$(MAKE) install
	@echo ""
	@echo "$(GREEN)✓ Проект настроен!$(NC)"
	@echo "$(BLUE)Следующие шаги:$(NC)"
	@echo "  1. Отредактируйте файл .env и добавьте API ключи"
	@echo "  2. Запустите бота: make run"

.DEFAULT_GOAL := help
