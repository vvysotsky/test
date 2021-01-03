from django.db import models

class Profile(models.Model):
    external_id = models.PositiveIntegerField (verbose_name='ID пользователя', unique=True,)
    name = models.TextField (verbose_name='Имя пользователя',)
    coach_information = models.TextField (verbose_name= 'Имя и контакты наставника',)

    def __str__(self):
        return f'{self.name}'


    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'       
