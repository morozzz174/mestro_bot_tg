# MESTRO Telegram Poster

Автоматическая публикация постов о приложении MESTRO в Telegram-группу.

## Как работает

1. GitHub Actions запускает скрипт каждый день в 07:08 UTC
2. Скрипт берёт следующий пост из `posts.py`
3. Отправляет его в Telegram-группу через Bot API
4. После 35 постов — цикл повторяется

## Настройка

1. Создайте бота через [@BotFather](https://t.me/BotFather)
2. Добавьте бота в группу администратором
3. Добавьте Secrets в GitHub:
   - `TELEGRAM_BOT_TOKEN` — токен бота
   - `TELEGRAM_CHAT_ID` — ID группы
4. Запустите вручную через Actions → `Telegram Daily Post` → `Run workflow`
