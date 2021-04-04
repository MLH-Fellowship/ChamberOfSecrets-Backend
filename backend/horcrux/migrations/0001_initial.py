# Generated by Django 2.2.19 on 2021-04-04 08:58

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
            name='FileUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_uploaded', models.FileField(upload_to='files/')),
            ],
        ),
        migrations.CreateModel(
            name='FileData',
            fields=[
                ('file_id', models.AutoField(primary_key=True, serialize=False)),
                ('file_name', models.CharField(max_length=1024)),
                ('upload_date', models.DateTimeField(auto_now=True)),
                ('upload_file_name', models.CharField(max_length=1030)),
                ('split_1', models.TextField()),
                ('split_2', models.TextField()),
                ('split_3', models.TextField()),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
            options={
                'ordering': ['file_id'],
                'unique_together': {('username', 'file_id')},
            },
        ),
    ]
