# Generated by Django 5.0.6 on 2024-06-12 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_delete_choice_delete_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogFilesEncrypted',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField()),
                ('filename', models.CharField(max_length=255)),
                ('saved_month', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
