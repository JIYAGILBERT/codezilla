# Generated by Django 5.1.7 on 2025-05-20 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capp', '0003_remove_question_choice1_remove_question_choice2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='published',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='question',
            name='published',
            field=models.BooleanField(default=True),
        ),
    ]
