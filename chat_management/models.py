from django.db import models

# Create your models here.
from users.models import UserAccount
import uuid
from django.utils import timezone


class Chat(models.Model):
    initiator = models.ForeignKey(
        UserAccount,
        on_delete=models.DO_NOTHING,
        related_name="initiator_chat",
        null=True,
    )
    acceptor = models.ForeignKey(
        UserAccount,
        on_delete=models.DO_NOTHING,
        related_name="acceptor_name",
        null=True,
    )
    short_id = models.CharField(max_length=255, default=uuid.uuid4, unique=True)


class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(UserAccount, on_delete=models.DO_NOTHING)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
