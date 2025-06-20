# Generated by Django 5.2.2 on 2025-06-11 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='created_at',
        ),
        migrations.AddField(
            model_name='question',
            name='category',
            field=models.CharField(default='General', max_length=100),
        ),
        migrations.AlterField(
            model_name='question',
            name='correct_option',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='option1',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='question',
            name='option2',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='question',
            name='option3',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='question',
            name='option4',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.TextField(),
        ),
    ]
