# Generated by Django 5.0.6 on 2024-05-18 16:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RoomLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField()),
                ('link', models.SlugField(unique=True)),
                ('first_message', models.TextField()),
                ('link_password', models.CharField(max_length=25)),
                ('is_open', models.BooleanField(default=True)),
                ('verified_ips', models.CharField(default='127.0.0.1', max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField()),
                ('message', models.CharField(max_length=250)),
                ('recorded_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('room_link', models.ForeignKey(default='10', on_delete=django.db.models.deletion.CASCADE, to='main.roomlink')),
            ],
            options={
                'ordering': ['-recorded_at'],
            },
        ),
    ]
