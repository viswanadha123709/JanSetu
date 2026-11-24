from django.contrib import admin
from apps.eligibility.models import Conversation

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_id', 'question_preview', 'language', 'timestamp')
    list_filter = ('language', 'timestamp')
    search_fields = ('question', 'answer', 'session_id')

    def question_preview(self, obj):
        return obj.question[:50]
