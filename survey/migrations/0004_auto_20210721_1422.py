# Generated by Django 3.2.5 on 2021-07-21 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0003_auto_20210721_1421'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'verbose_name': 'Respuesta', 'verbose_name_plural': 'Respuestas'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': 'Pregunta', 'verbose_name_plural': 'Preguntas'},
        ),
    ]