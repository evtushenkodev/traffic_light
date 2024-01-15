import asyncio
import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from bot.telegram_bot import bot

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "launching bot"

    def handle(self, *args, **options):
        try:
            asyncio.run(bot.infinity_polling(logger_level=settings.LOG_LEVEL))
        except Exception as e:
            logger.error(f"Exception: {e}")
