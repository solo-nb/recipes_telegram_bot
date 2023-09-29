import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipes_telegram_bot.settings')
if not settings.configured:
    django.setup()


from datacenter.dispatcher import run_pooling


if __name__ == "__main__":
   
    run_pooling()
