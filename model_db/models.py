from django.db import models




class Chat(models.Model):

    chat_name = models.CharField(max_length=120, unique=True)

    def __str__(self) -> str:
        return self.chat_name


class Trigger(models.Model):

    trigger_name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.trigger_name

class Recipent(models.Model):

    chat_name = models.CharField(max_length=120, unique=True)

    def __str__(self) -> str:
        return self.chat_name