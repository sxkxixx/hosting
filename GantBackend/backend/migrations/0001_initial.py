# Generated by Django 4.1.7 on 2023-03-14 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=100, verbose_name='Название задачи')),
                ('task_description', models.CharField(max_length=200, null=True, verbose_name='Описание задачи')),
                ('start_date', models.DateTimeField(verbose_name='Старт задачи')),
                ('deadline', models.DateTimeField(verbose_name='Дедлайн задачи')),
                ('status', models.CharField(choices=[('PLANNED', 'Запланирована'), ('TO WORK', 'В работу'), ('IN WORK', 'В работе'), ('COMPLETED', 'Завершена')], max_length=20, verbose_name='Статус задачи')),
            ],
        ),
    ]
