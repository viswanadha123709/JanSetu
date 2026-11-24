from django.db import models
from django.contrib.auth.models import User
from apps.schemes.models import Scheme, Policy

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='conversations')
    session_id = models.CharField(max_length=100, db_index=True)
    question = models.TextField()
    answer = models.TextField()
    language = models.CharField(max_length=10, default='en')
    related_scheme = models.ForeignKey(Scheme, on_delete=models.SET_NULL, null=True, blank=True)
    related_policy = models.ForeignKey(Policy, on_delete=models.SET_NULL, null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        user_str = self.user.username if self.user else f"Guest ({self.session_id[:8]})"
        return f"{user_str} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}: {self.question[:40]}..."
