
from django.db import models




class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='ID пользователя в соц сети',
        unique=True
    )
    name = models.TextField(
        verbose_name='Имя пользователя'
    )

    bot_admin = models.BooleanField(default=False)

    def __str__(self):
        return f'#{self.external_id}{self.name}'



    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

class Message(models.Model):
    profile = models.ForeignKey(to='tg_bot.Profile',
                                verbose_name='Профиль',
                                on_delete=models.PROTECT,
                                )
    text = models.TextField(
        verbose_name='Текст'
    )
    created_at = models.DateTimeField(
        verbose_name='Время полученя сообщения',
        auto_now_add=True
    )

    def __str__(self):
        return f'Сообщение {self.pk} от {self.profile}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

class Tg_response_msg(models.Model):
    command = models.CharField(max_length=255, verbose_name='Команда', unique=True)
    content = models.TextField(verbose_name='Текст ответа')

    class Meta:
        verbose_name = 'Ответ на команду'
        verbose_name_plural = 'Ответы на команды'