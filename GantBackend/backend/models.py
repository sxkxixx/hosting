from django.db import models

# Create your models here.


class Task(models.Model):
    STATUS_CHOICE = [
        ('PLANNED', 'Запланирована'),
        ('TO WORK', 'В работу'),
        ('IN WORK', 'В работе'),
        ('COMPLETED', 'Завершена'),
    ]

    task_name = models.CharField(verbose_name='Название задачи', max_length=100)
    task_description = models.CharField(verbose_name='Описание задачи', max_length=200, null=True, blank=True)
    start_date = models.DateTimeField(verbose_name='Старт задачи', null=False)
    deadline = models.DateTimeField(verbose_name='Дедлайн задачи', null=False)
    status = models.CharField(verbose_name='Статус задачи', choices=STATUS_CHOICE, max_length=20, null=False)

    def __str__(self):
        return self.task_name

