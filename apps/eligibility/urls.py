from django.urls import path
from apps.eligibility.views import ChatAdvisorView, ConversationHistoryView

urlpatterns = [
    path('chat/', ChatAdvisorView.as_view(), name='eligibility_chat'),
    path('history/', ConversationHistoryView.as_view(), name='eligibility_history'),
]
