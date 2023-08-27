import telegram_bot
import os

if __name__ == "__main__":
    BOT_TOKEN = os.environ['BOT_TOKEN']
    telegram_bot.run(BOT_TOKEN)