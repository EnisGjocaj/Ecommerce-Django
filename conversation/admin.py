from django.contrib import admin

from .models import ConversationMessages, Conversation


admin.site.register(ConversationMessages)
admin.site.register(Conversation)
