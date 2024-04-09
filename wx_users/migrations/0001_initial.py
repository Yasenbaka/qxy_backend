# Generated by Django 5.0.3 on 2024-04-08 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WxUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('openid', models.CharField(max_length=255, unique=True)),
                ('nickname', models.CharField(blank=True, max_length=255)),
                ('avatar_url', models.URLField(blank=True)),
            ],
        ),
    ]