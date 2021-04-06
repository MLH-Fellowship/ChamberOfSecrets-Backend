# Generated by Django 2.2.19 on 2021-04-06 17:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_key', models.TextField()),
                ('auth_per_upload', models.BooleanField(default=False)),
                ('gdrive_token', models.TextField(blank=True)),
                ('dropbox_token', models.TextField(blank=True)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username', unique=True)),
            ],
        ),
    ]
