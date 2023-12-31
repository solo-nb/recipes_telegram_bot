# Generated by Django 4.2.5 on 2023-09-28 12:54

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('telegram_id', models.IntegerField(default=False, unique=True)),
                ('username', models.CharField(max_length=64, null=True, verbose_name='UserName')),
                ('name', models.CharField(max_length=256, null=True, verbose_name='Имя')),
                ('is_admin', models.BooleanField(blank=True, default=False, null=True, verbose_name='Администратор')),
                ('registration', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
    ]
