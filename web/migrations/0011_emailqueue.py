# Generated by Django 5.0.7 on 2024-07-26 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_pendingregistration_delete_fileversion'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailQueue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('sent', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]