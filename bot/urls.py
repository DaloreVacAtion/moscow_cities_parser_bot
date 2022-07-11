from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .bot import WebhookBotView

bot_urls = [
    path('', csrf_exempt(WebhookBotView.as_view()),)
]
